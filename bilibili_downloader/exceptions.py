"""
自定义异常类
"""


class BilibiliDownloadError(Exception):
    """B站下载基础异常类"""
    pass


class VideoNotFoundError(BilibiliDownloadError):
    """视频未找到异常"""
    pass


class DurationExceededError(BilibiliDownloadError):
    """视频时长超出限制异常"""
    pass


class NetworkError(BilibiliDownloadError):
    """网络请求异常"""
    pass


class FFmpegError(BilibiliDownloadError):
    """FFmpeg处理异常"""
    pass