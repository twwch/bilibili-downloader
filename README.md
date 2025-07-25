# Bilibili Downloader

[![PyPI version](https://badge.fury.io/py/bilibili-downloader.svg)](https://badge.fury.io/py/bilibili-downloader)
[![Python Version](https://img.shields.io/pypi/pyversions/bilibili-downloader.svg)](https://pypi.org/project/bilibili-downloader/)
[![License](https://img.shields.io/github/license/twwch/bilibili-downloader)](https://github.com/twwch/bilibili-downloader/blob/main/LICENSE)
[![CI](https://github.com/twwch/bilibili-downloader/actions/workflows/ci.yml/badge.svg)](https://github.com/twwch/bilibili-downloader/actions/workflows/ci.yml)
[![Downloads](https://pepy.tech/badge/bilibili-downloader)](https://pepy.tech/project/bilibili-downloader)

一个简单易用的B站视频下载Python库，支持下载视频和音频。

## 特性

- 支持下载B站视频（包括音视频合并）
- 支持仅下载音频并转换格式（mp3, wav, m4a）
- 支持分P视频下载
- 自动处理短链接跳转
- 支持设置最大下载时长限制
- 异步下载，提高效率
- 清晰的错误处理

## 安装

```bash
# 安装依赖
pip install aiohttp httpx requests ffmpy3
```

注意：还需要安装FFmpeg并确保在系统PATH中可用。

## 快速开始

### 基础用法

```python
from bilibili_downloader import BilibiliDownloader

# 创建下载器实例
downloader = BilibiliDownloader()

# 下载音频
result = downloader.download_audio("https://www.bilibili.com/video/BV1xx411c7mD")
if result.success:
    print(f"下载成功: {result.file_path}")
else:
    print(f"下载失败: {result.message}")

# 下载视频
result = downloader.download_video("https://www.bilibili.com/video/BV1xx411c7mD")
if result.success:
    print(f"下载成功: {result.file_path}")
```

### 高级配置

```python
# 使用认证信息（可选，用于下载高清视频）
downloader = BilibiliDownloader(
    sessdata="your_sessdata",
    bili_jct="your_bili_jct",
    buvid3="your_buvid3",
    download_dir="./my_downloads",
    ffmpeg_path="/usr/local/bin/ffmpeg",
    max_duration=7200  # 最大2小时
)

# 指定输出路径和格式
result = downloader.download_audio(
    "https://www.bilibili.com/video/BV1xx411c7mD",
    output_path="./output/audio.mp3",
    audio_format="mp3"
)

# 获取视频信息
video_info = downloader.get_video_info("https://www.bilibili.com/video/BV1xx411c7mD")
print(f"标题: {video_info.title}")
print(f"时长: {video_info.duration}秒")

# 检查视频时长
ok, msg, duration = downloader.check_duration("https://www.bilibili.com/video/BV1xx411c7mD")
if ok:
    print(f"视频时长: {duration}秒")
else:
    print(f"错误: {msg}")
```

### 异步使用

```python
import asyncio

async def download_multiple():
    downloader = BilibiliDownloader()
    
    urls = [
        "https://www.bilibili.com/video/BV1xx411c7mD",
        "https://www.bilibili.com/video/BV1yy4y1k7VD",
    ]
    
    tasks = [downloader.download_audio_async(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        if result.success:
            print(f"下载成功: {result.file_path}")
        else:
            print(f"下载失败: {result.message}")

# 运行异步下载
asyncio.run(download_multiple())
```

## API 参考

### BilibiliDownloader

#### 初始化参数

- `sessdata` (str): B站Cookie中的SESSDATA，用于认证
- `bili_jct` (str): B站Cookie中的bili_jct
- `buvid3` (str): B站Cookie中的buvid3
- `download_dir` (str): 下载目录，默认"./downloads"
- `ffmpeg_path` (str): FFmpeg路径，不指定则自动查找
- `max_duration` (int): 最大允许下载时长（秒），默认10800（3小时）

#### 方法

- `get_video_info(url: str) -> VideoInfo`: 获取视频信息
- `download_audio(url: str, output_path: str = None, audio_format: str = "mp3") -> DownloadResult`: 下载音频
- `download_video(url: str, output_path: str = None, video_format: str = "mp4") -> DownloadResult`: 下载视频
- `check_duration(url: str) -> Tuple[bool, str, int]`: 检查视频时长

### 数据模型

#### VideoInfo
- `bvid`: 视频BV号
- `title`: 视频标题
- `duration`: 视频时长（秒）
- `video_url`: 视频流URL
- `audio_url`: 音频流URL
- `page`: 分P号

#### DownloadResult
- `success`: 是否成功
- `message`: 结果消息
- `file_path`: 下载文件路径
- `duration`: 视频时长
- `video_info`: 视频信息对象

## 异常处理

SDK定义了以下异常类：

- `BilibiliDownloadError`: 基础异常类
- `VideoNotFoundError`: 视频未找到
- `DurationExceededError`: 视频时长超出限制
- `NetworkError`: 网络请求失败
- `FFmpegError`: FFmpeg处理失败

```python
from bilibili_downloader import BilibiliDownloader, VideoNotFoundError, DurationExceededError

downloader = BilibiliDownloader(max_duration=3600)  # 1小时限制

try:
    result = downloader.download_audio("https://www.bilibili.com/video/BV1xx411c7mD")
except VideoNotFoundError:
    print("视频不存在")
except DurationExceededError:
    print("视频时长超过限制")
except Exception as e:
    print(f"下载失败: {e}")
```

## 注意事项

1. 需要安装FFmpeg才能正常使用
2. 下载高清视频可能需要提供Cookie认证信息
3. 请遵守B站的使用条款，合理使用下载功能
4. 默认限制最大下载时长为3小时，可通过参数调整

## License

MIT