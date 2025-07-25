"""
数据模型定义
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class VideoInfo:
    """视频信息"""
    bvid: str
    title: str
    duration: int  # 秒
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    page: int = 1


@dataclass
class DownloadResult:
    """下载结果"""
    success: bool
    message: str
    file_path: Optional[str] = None
    duration: Optional[int] = None
    video_info: Optional[VideoInfo] = None