#!/bin/bash
set -e

echo "🚀 开始发布 bilibili-downloader-sdk..."

# 检查是否在正确的目录
if [ ! -f "setup.py" ]; then
    echo "❌ 错误：请在包根目录运行此脚本"
    exit 1
fi

# 清理旧文件
echo "📦 清理旧的构建文件..."
rm -rf build/ dist/ *.egg-info/

# 构建
echo "🔨 构建分发包..."
python -m build

# 检查
echo "✅ 检查包质量..."
twine check dist/*

# 显示包信息
echo "📋 包信息："
ls -lh dist/

# 询问是否继续
read -p "是否发布到 TestPyPI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📤 上传到 TestPyPI..."
    twine upload --repository testpypi dist/*
    echo "✅ 已发布到 TestPyPI"
    echo "🧪 测试安装命令："
    echo "pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ bilibili-downloader-sdk"
    echo ""
    read -p "按回车继续..."
fi

read -p "是否发布到正式 PyPI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "⚠️  最后确认：即将发布到正式 PyPI"
    read -p "确定要继续吗? (yes/no) " -r
    if [[ $REPLY == "yes" ]]; then
        echo "📤 上传到 PyPI..."
        twine upload dist/*
        echo "✅ 发布成功！"
        echo "📦 安装命令：pip install bilibili-downloader-sdk"
        echo "🌐 查看项目：https://pypi.org/project/bilibili-downloader-sdk/"
    else
        echo "❌ 已取消发布"
    fi
fi

echo "✨ 完成！"