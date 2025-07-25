# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added
- 初始版本发布
- 支持下载B站视频（音视频合并）
- 支持仅下载音频并转换格式（mp3, wav, m4a）
- 支持分P视频下载
- 异步下载功能
- 自动处理短链接跳转
- 可配置的下载时长限制
- 完善的错误处理机制
- 详细的使用文档和示例

### Features
- `BilibiliDownloader` 主类
- `download_video()` - 下载完整视频
- `download_audio()` - 仅下载音频
- `get_video_info()` - 获取视频信息
- `check_duration()` - 检查视频时长
- 异步版本的所有方法

### Security
- 安全的文件名处理
- 请求超时保护
- 文件大小限制