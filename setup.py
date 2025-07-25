"""
Bilibili Downloader SDK setup.py
"""
from setuptools import setup, find_packages
import os

# 读取README文件
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取requirements.txt
def read_requirements():
    with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="bilibili-downloader",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="一个简单易用的B站视频下载Python库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/twwch/bilibili-downloader",
    packages=find_packages(exclude=["tests*", "docs*", "examples*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="bilibili video download audio api",
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "twine>=4.0.0",
            "wheel>=0.38.0",
            "build>=0.10.0",
        ]
    },
    project_urls={
        "Bug Reports": "https://github.com/twwch/bilibili-downloader/issues",
        "Source": "https://github.com/twwch/bilibili-downloader",
        "Documentation": "https://github.com/twwch/bilibili-downloader#readme",
    },
    include_package_data=True,
    zip_safe=False,
)