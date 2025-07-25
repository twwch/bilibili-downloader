"""
B站视频下载器核心实现
"""
import asyncio
import datetime
import json
import os
import re
import time
from typing import Optional, Tuple, Dict, Any

import aiohttp
import httpx
import requests
from ffmpy3 import FFmpeg

from .exceptions import (
    BilibiliDownloadError,
    VideoNotFoundError,
    DurationExceededError,
    NetworkError,
    FFmpegError
)
from .models import VideoInfo, DownloadResult
from .utils import extract_bvid, extract_page_number, get_ffmpeg_path, parse_bili_url


class BilibiliDownloader:
    """B站视频下载器"""
    
    def __init__(
        self,
        sessdata: str = "",
        bili_jct: str = "",
        buvid3: str = "",
        download_dir: str = "./downloads",
        ffmpeg_path: Optional[str] = None,
        max_duration: int = 10800  # 默认最大时长3小时
    ):
        """
        初始化下载器
        
        Args:
            sessdata: B站Cookie中的SESSDATA
            bili_jct: B站Cookie中的bili_jct
            buvid3: B站Cookie中的buvid3
            download_dir: 下载目录
            ffmpeg_path: FFmpeg路径，不指定则自动查找
            max_duration: 最大允许下载时长（秒）
        """
        self.sessdata = sessdata
        self.bili_jct = bili_jct
        self.buvid3 = buvid3
        self.download_dir = download_dir
        self.ffmpeg_path = ffmpeg_path or get_ffmpeg_path()
        self.max_duration = max_duration
        
        # 创建下载目录
        os.makedirs(self.download_dir, exist_ok=True)
        
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.bilibili.com"
        }
        
        # 如果提供了认证信息，添加到Cookie
        if sessdata:
            self.headers["Cookie"] = f"SESSDATA={sessdata}; bili_jct={bili_jct}; buvid3={buvid3}"
    
    def get_video_info(self, url: str) -> VideoInfo:
        """
        获取视频信息
        
        Args:
            url: B站视频URL
            
        Returns:
            VideoInfo: 视频信息对象
            
        Raises:
            VideoNotFoundError: 视频未找到
            NetworkError: 网络请求失败
        """
        bvid, page = parse_bili_url(url)
        if not bvid:
            raise VideoNotFoundError(f"无法从URL中提取BV号: {url}")
        
        try:
            # 获取视频页面
            resp = requests.get(url, headers=self.headers, timeout=10)
            resp.raise_for_status()
            
            # 提取标题
            title = ""
            for pattern in [
                r'<h1 title="(.*?)" class="video-title"',
                r'<title data-vue-meta="true">(.*?)</title>',
                r'<meta data-vue-meta="true" itemprop="name" name="title" content="(.*?)">',
                r'<meta data-vue-meta="true" property="og:title" content="(.*?)">'
            ]:
                match = re.search(pattern, resp.text)
                if match:
                    title = match.group(1)
                    break
            
            # 提取播放信息
            playinfo_match = re.search(r'<script>window.__playinfo__=(.*?)</script>', resp.text)
            if playinfo_match:
                playinfo = json.loads(playinfo_match.group(1))
                video_url = playinfo['data']['dash']['video'][0]['base_url']
                
                # 选择音质最低的音频（文件最小）
                audio_list = playinfo['data']['dash']['audio']
                audio_url = min(audio_list, key=lambda x: x.get('bandwidth', 0))['base_url']
                
                duration = playinfo['data'].get('timelength', 0) // 1000
            else:
                # 使用API获取
                video_url, audio_url, duration = self._get_info_from_api(bvid)
            
            return VideoInfo(
                bvid=bvid,
                title=title or f"BV{bvid}",
                duration=duration,
                video_url=video_url,
                audio_url=audio_url,
                page=page
            )
            
        except requests.RequestException as e:
            raise NetworkError(f"获取视频信息失败: {e}")
        except (json.JSONDecodeError, KeyError) as e:
            raise BilibiliDownloadError(f"解析视频信息失败: {e}")
    
    def _get_info_from_api(self, bvid: str) -> Tuple[str, str, int]:
        """通过API获取视频信息"""
        api_url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
        
        try:
            resp = requests.get(api_url, headers=self.headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if data['code'] != 0:
                raise VideoNotFoundError(f"API返回错误: {data.get('message', 'Unknown error')}")
            
            cid = data['data']['cid']
            
            # 获取播放URL
            playurl_api = f'https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&qn=127&fnval=16'
            play_resp = requests.get(playurl_api, headers=self.headers, timeout=10)
            play_resp.raise_for_status()
            play_data = play_resp.json()
            
            if play_data['code'] != 0:
                raise BilibiliDownloadError(f"获取播放URL失败: {play_data.get('message', 'Unknown error')}")
            
            dash_data = play_data['data']['dash']
            video_url = dash_data['video'][0]['base_url']
            audio_url = dash_data['audio'][0]['base_url']
            duration = dash_data.get('duration', 0)
            
            return video_url, audio_url, duration
            
        except requests.RequestException as e:
            raise NetworkError(f"API请求失败: {e}")
    
    async def _download_file(self, url: str, filepath: str, description: str = "文件"):
        """异步下载文件"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(filepath, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r下载{description}: {progress:.1f}%", end='')
                
                print()  # 换行
    
    def _convert_to_audio(self, input_file: str, output_file: str, audio_format: str = "mp3"):
        """转换为音频格式"""
        try:
            ff = FFmpeg(
                executable=self.ffmpeg_path,
                global_options=['-y'],
                inputs={input_file: None},
                outputs={output_file: f'-acodec libmp3lame -ab 128k' if audio_format == 'mp3' else None}
            )
            ff.run()
            
            # 删除临时文件
            if os.path.exists(input_file):
                os.remove(input_file)
                
        except Exception as e:
            raise FFmpegError(f"音频转换失败: {e}")
    
    async def download_audio_async(self, url: str, output_path: Optional[str] = None, audio_format: str = "mp3") -> DownloadResult:
        """
        异步下载音频
        
        Args:
            url: B站视频URL
            output_path: 输出文件路径，不指定则自动生成
            audio_format: 音频格式，支持 mp3, wav, m4a
            
        Returns:
            DownloadResult: 下载结果
        """
        try:
            # 获取视频信息
            video_info = self.get_video_info(url)
            
            # 检查时长限制
            if video_info.duration > self.max_duration:
                raise DurationExceededError(
                    f"视频时长({video_info.duration}秒)超过限制({self.max_duration}秒)"
                )
            
            # 生成文件名
            if not output_path:
                safe_title = re.sub(r'[<>:"/\\|?*]', '_', video_info.title)[:50]
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = os.path.join(
                    self.download_dir,
                    f"{safe_title}_{timestamp}.{audio_format}"
                )
            
            # 下载音频流
            temp_audio = os.path.join(self.download_dir, f"temp_audio_{video_info.bvid}.m4s")
            await self._download_file(video_info.audio_url, temp_audio, "音频")
            
            # 转换格式
            self._convert_to_audio(temp_audio, output_path, audio_format)
            
            return DownloadResult(
                success=True,
                message="下载成功",
                file_path=output_path,
                duration=video_info.duration,
                video_info=video_info
            )
            
        except Exception as e:
            return DownloadResult(
                success=False,
                message=str(e)
            )
    
    def download_audio(self, url: str, output_path: Optional[str] = None, audio_format: str = "mp3") -> DownloadResult:
        """
        同步下载音频
        
        Args:
            url: B站视频URL
            output_path: 输出文件路径
            audio_format: 音频格式
            
        Returns:
            DownloadResult: 下载结果
        """
        return asyncio.run(self.download_audio_async(url, output_path, audio_format))
    
    async def download_video_async(self, url: str, output_path: Optional[str] = None, video_format: str = "mp4") -> DownloadResult:
        """
        异步下载视频
        
        Args:
            url: B站视频URL
            output_path: 输出文件路径
            video_format: 视频格式
            
        Returns:
            DownloadResult: 下载结果
        """
        try:
            # 获取视频信息
            video_info = self.get_video_info(url)
            
            # 检查时长限制
            if video_info.duration > self.max_duration:
                raise DurationExceededError(
                    f"视频时长({video_info.duration}秒)超过限制({self.max_duration}秒)"
                )
            
            # 生成文件名
            if not output_path:
                safe_title = re.sub(r'[<>:"/\\|?*]', '_', video_info.title)[:50]
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = os.path.join(
                    self.download_dir,
                    f"{safe_title}_{timestamp}.{video_format}"
                )
            
            # 下载视频和音频流
            temp_video = os.path.join(self.download_dir, f"temp_video_{video_info.bvid}.m4s")
            temp_audio = os.path.join(self.download_dir, f"temp_audio_{video_info.bvid}.m4s")
            
            # 并发下载
            await asyncio.gather(
                self._download_file(video_info.video_url, temp_video, "视频"),
                self._download_file(video_info.audio_url, temp_audio, "音频")
            )
            
            # 合并视频和音频
            try:
                ff = FFmpeg(
                    executable=self.ffmpeg_path,
                    global_options=['-y'],
                    inputs={temp_video: None, temp_audio: None},
                    outputs={output_path: '-c:v copy -c:a copy'}
                )
                ff.run()
                
                # 删除临时文件
                for temp_file in [temp_video, temp_audio]:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                        
            except Exception as e:
                raise FFmpegError(f"视频合并失败: {e}")
            
            return DownloadResult(
                success=True,
                message="下载成功",
                file_path=output_path,
                duration=video_info.duration,
                video_info=video_info
            )
            
        except Exception as e:
            return DownloadResult(
                success=False,
                message=str(e)
            )
    
    def download_video(self, url: str, output_path: Optional[str] = None, video_format: str = "mp4") -> DownloadResult:
        """
        同步下载视频
        
        Args:
            url: B站视频URL
            output_path: 输出文件路径
            video_format: 视频格式
            
        Returns:
            DownloadResult: 下载结果
        """
        return asyncio.run(self.download_video_async(url, output_path, video_format))
    
    def check_duration(self, url: str) -> Tuple[bool, str, int]:
        """
        检查视频时长
        
        Args:
            url: B站视频URL
            
        Returns:
            Tuple[bool, str, int]: (是否在限制内, 消息, 时长秒数)
        """
        try:
            video_info = self.get_video_info(url)
            
            if video_info.duration > self.max_duration:
                return False, f"视频时长({video_info.duration}秒)超过限制({self.max_duration}秒)", video_info.duration
            
            return True, "ok", video_info.duration
            
        except Exception as e:
            return False, str(e), 0