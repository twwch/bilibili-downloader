"""
Bilibili Downloader SDK
一个简单易用的B站视频下载SDK
"""

from .downloader import BilibiliDownloader
from .models import VideoInfo, DownloadResult
from .exceptions import BilibiliDownloadError, VideoNotFoundError, DurationExceededError

__version__ = "1.0.0"
__all__ = [
    "BilibiliDownloader",
    "VideoInfo",
    "DownloadResult",
    "BilibiliDownloadError",
    "VideoNotFoundError",
    "DurationExceededError"
]