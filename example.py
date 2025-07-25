"""
Bilibili Downloader SDK 使用示例
"""
import asyncio
from bilibili_downloader import BilibiliDownloader, VideoNotFoundError, DurationExceededError


def example_basic():
    """基础使用示例"""
    print("=== 基础使用示例 ===")
    
    # 创建下载器
    downloader = BilibiliDownloader()
    
    # 测试URL
    test_url = "https://www.bilibili.com/video/BV1xx411c7mD"
    
    # 获取视频信息
    try:
        video_info = downloader.get_video_info(test_url)
        print(f"视频标题: {video_info.title}")
        print(f"视频时长: {video_info.duration}秒")
        print(f"BV号: {video_info.bvid}")
    except VideoNotFoundError:
        print("视频未找到")
        return
    
    # 下载音频
    print("\n开始下载音频...")
    result = downloader.download_audio(test_url, audio_format="mp3")
    if result.success:
        print(f"音频下载成功: {result.file_path}")
    else:
        print(f"音频下载失败: {result.message}")


def example_advanced():
    """高级使用示例"""
    print("\n=== 高级使用示例 ===")
    
    # 使用自定义配置创建下载器
    downloader = BilibiliDownloader(
        download_dir="./my_downloads",
        max_duration=1800  # 30分钟限制
    )
    
    # 检查多个视频
    urls = [
        "https://www.bilibili.com/video/BV1xx411c7mD",
        "https://b23.tv/abcdefg",  # 短链接示例
        "https://www.bilibili.com/video/BV1xx411c7mD?p=2"  # 分P视频
    ]
    
    for url in urls:
        print(f"\n检查视频: {url}")
        ok, msg, duration = downloader.check_duration(url)
        if ok:
            print(f"✓ 可以下载，时长: {duration}秒")
        else:
            print(f"✗ 无法下载: {msg}")


async def example_async():
    """异步下载示例"""
    print("\n=== 异步下载示例 ===")
    
    downloader = BilibiliDownloader()
    
    # 多个视频URL
    urls = [
        "https://www.bilibili.com/video/BV1xx411c7mD",
        "https://www.bilibili.com/video/BV1yy4y1k7VD",
    ]
    
    # 创建异步任务
    tasks = []
    for i, url in enumerate(urls):
        # 为每个视频指定不同的输出文件名
        output_path = f"./downloads/video_{i+1}.mp3"
        task = downloader.download_audio_async(url, output_path)
        tasks.append(task)
    
    # 并发执行下载
    print("开始并发下载...")
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 处理结果
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"视频{i+1} 下载异常: {result}")
        elif result.success:
            print(f"视频{i+1} 下载成功: {result.file_path}")
        else:
            print(f"视频{i+1} 下载失败: {result.message}")


def example_error_handling():
    """错误处理示例"""
    print("\n=== 错误处理示例 ===")
    
    # 设置严格的时长限制
    downloader = BilibiliDownloader(max_duration=60)  # 1分钟
    
    test_cases = [
        "https://www.bilibili.com/video/invalid_url",  # 无效URL
        "https://www.bilibili.com/video/BV1234567890",  # 不存在的视频
        "https://www.bilibili.com/video/BV1xx411c7mD",  # 可能超时长的视频
    ]
    
    for url in test_cases:
        print(f"\n测试URL: {url}")
        try:
            result = downloader.download_audio(url)
            if result.success:
                print(f"下载成功: {result.file_path}")
            else:
                print(f"下载失败: {result.message}")
        except VideoNotFoundError as e:
            print(f"视频未找到: {e}")
        except DurationExceededError as e:
            print(f"视频时长超限: {e}")
        except Exception as e:
            print(f"其他错误: {e}")


def example_video_download():
    """视频下载示例"""
    print("\n=== 视频下载示例 ===")
    
    downloader = BilibiliDownloader()
    
    test_url = "https://www.bilibili.com/video/BV1xx411c7mD"
    
    print("开始下载视频（包含画面）...")
    result = downloader.download_video(test_url, video_format="mp4")
    
    if result.success:
        print(f"视频下载成功: {result.file_path}")
        print(f"视频信息:")
        print(f"  - 标题: {result.video_info.title}")
        print(f"  - 时长: {result.duration}秒")
        print(f"  - BV号: {result.video_info.bvid}")
    else:
        print(f"视频下载失败: {result.message}")


if __name__ == "__main__":
    # 运行各种示例
    example_basic()
    # example_advanced()
    # example_error_handling()
    # example_video_download()
    #
    # # 运行异步示例
    # print("\n" + "="*50)
    # asyncio.run(example_async())