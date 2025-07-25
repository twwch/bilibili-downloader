"""
工具函数
"""
import re
import os
from typing import Optional, Tuple


def extract_bvid(url: str) -> Optional[str]:
    """从URL中提取BV号"""
    pattern = r"(BV\w+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


def extract_page_number(url: str) -> int:
    """从URL中提取分P号"""
    query_params = {}
    if "?" in url:
        query_string = url.split("?")[1]
        for param in query_string.split("&"):
            if "=" in param:
                key, value = param.split("=", 1)
                query_params[key] = value
    
    page = query_params.get("p", "1")
    try:
        return int(page)
    except ValueError:
        return 1


def get_url_from_text(text: str) -> str:
    """从文本中提取URL"""
    url_pattern = r'https?://[\w\-]+\.[\w\-]+[/?\S]*'
    match = re.search(url_pattern, text)
    if match:
        return match.group()
    return ''


def parse_bili_url(url: str) -> Tuple[Optional[str], int]:
    """解析B站URL，返回BV号和分P号"""
    bvid = extract_bvid(url)
    page = extract_page_number(url)
    return bvid, page


def get_ffmpeg_path() -> str:
    """获取FFmpeg路径"""
    # 尝试从环境变量获取
    ffmpeg_path = os.environ.get('FFMPEG_PATH')
    if ffmpeg_path and os.path.exists(ffmpeg_path):
        return ffmpeg_path
    
    # 常见路径
    common_paths = [
        '/usr/bin/ffmpeg',
        '/usr/local/bin/ffmpeg',
        '/opt/homebrew/bin/ffmpeg',
        'ffmpeg'  # 系统PATH中
    ]
    
    for path in common_paths:
        if os.path.exists(path) or os.system(f'which {path} > /dev/null 2>&1') == 0:
            return path
    
    return 'ffmpeg'  # 默认假设在PATH中