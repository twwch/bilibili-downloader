# 发布到 PyPI 的完整指南

本文档详细说明如何将 bilibili-downloader 发布到 PyPI (Python Package Index)。

## 前置准备

### 1. 注册 PyPI 账号

1. 访问 [https://pypi.org/account/register/](https://pypi.org/account/register/) 注册正式账号
2. 访问 [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/) 注册测试账号（建议先在测试环境练习）
3. 在账号设置中启用双因素认证（2FA）以提高安全性

### 2. 生成 API Token

1. 登录 PyPI 账号
2. 进入账号设置 -> API tokens
3. 点击 "Add API token"
4. 设置 token 名称和作用域
5. 保存生成的 token（只显示一次）

### 3. 配置认证信息

创建 `~/.pypirc` 文件：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = 

[testpypi]
username = __token__
password = 
```

确保文件权限安全：
```bash
chmod 600 ~/.pypirc
```

## 发布步骤

### 1. 安装发布工具

```bash
pip install --upgrade pip setuptools wheel twine build
```

### 2. 检查包名是否可用

访问 https://pypi.org/project/bilibili-downloader/ 确认包名未被占用。
如果已被占用，需要在 `setup.py` 和 `pyproject.toml` 中修改包名。

### 3. 更新版本信息

在发布前，确保更新：
- `setup.py` 中的 version
- `pyproject.toml` 中的 version
- `__init__.py` 中的 __version__
- 填写正确的 author 和 author_email

### 4. 构建分发包

```bash
# 清理之前的构建
rm -rf build/ dist/ *.egg-info/

# 构建源码分发包和wheel包
python -m build
```

这会在 `dist/` 目录下生成：
- `bilibili-downloader-1.0.0.tar.gz` (源码包)
- `bilibili_downloader-1.0.0-py3-none-any.whl` (wheel包)

### 5. 检查包内容

```bash
# 检查包的元数据
twine check dist/*

# 查看包内容
tar -tzf dist/bilibili-downloader-1.0.0.tar.gz
```

### 6. 发布到测试 PyPI（推荐）

先发布到测试服务器验证：

```bash
twine upload --repository testpypi dist/*
```

测试安装：
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ bilibili-downloader
```

### 7. 发布到正式 PyPI

确认测试无误后，发布到正式环境：

```bash
twine upload dist/*
```

### 8. 验证发布

```bash
# 等待几分钟让 PyPI 更新索引
pip install bilibili-downloader

# 测试导入
python -c "import bilibili_downloader; print(bilibili_downloader.__version__)"
```

## 自动化发布脚本

创建 `publish.sh` 脚本简化流程：

```bash
#!/bin/bash
set -e

echo "🚀 开始发布 bilibili-downloader..."

# 清理旧文件
echo "📦 清理旧的构建文件..."
rm -rf build/ dist/ *.egg-info/

# 构建
echo "🔨 构建分发包..."
python -m build

# 检查
echo "✅ 检查包质量..."
twine check dist/*

# 询问是否继续
read -p "是否发布到 TestPyPI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📤 上传到 TestPyPI..."
    twine upload --repository testpypi dist/*
    echo "✅ 已发布到 TestPyPI"
    echo "🧪 测试安装命令："
    echo "pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ bilibili-downloader"
fi

read -p "是否发布到正式 PyPI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📤 上传到 PyPI..."
    twine upload dist/*
    echo "✅ 发布成功！"
    echo "📦 安装命令：pip install bilibili-downloader"
fi
```

## 版本管理

### 语义化版本控制

遵循语义化版本规范 (SemVer)：
- 主版本号：不兼容的 API 修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

示例：`1.0.0` -> `1.0.1` (修复bug) -> `1.1.0` (新功能) -> `2.0.0` (重大改变)

### 更新版本的位置

发布新版本时，需要更新以下文件中的版本号：
1. `setup.py` 中的 `version=`
2. `pyproject.toml` 中的 `version =`
3. `__init__.py` 中的 `__version__ =`

## 常见问题

### 1. 包名已存在
- 解决：更改包名，如 `bilibili-video-downloader` 或添加用户名前缀

### 2. 认证失败
- 确认使用 `__token__` 作为用户名
- 确认 token 以 `pypi-` 开头
- 检查是否复制了完整的 token

### 3. 包内容缺失
- 检查 `MANIFEST.in` 文件
- 确认 `include_package_data=True` 在 setup.py 中

### 4. 依赖安装失败
- 确保所有依赖都在 PyPI 上可用
- 检查依赖版本兼容性

## 维护建议

1. **版本发布前检查清单**：
   - [ ] 更新版本号
   - [ ] 更新 CHANGELOG
   - [ ] 运行所有测试
   - [ ] 更新文档
   - [ ] 检查依赖版本

2. **使用 GitHub Actions 自动发布**：
   可以配置 CI/CD 在创建 tag 时自动发布

3. **保持向后兼容**：
   尽量避免破坏性更改，如必须，在文档中明确说明

4. **定期更新依赖**：
   保持依赖库的更新，但要测试兼容性

## 相关链接

- [PyPI 官方文档](https://packaging.python.org/tutorials/packaging-projects/)
- [Twine 文档](https://twine.readthedocs.io/)
- [语义化版本](https://semver.org/lang/zh-CN/)
- [Python 打包用户指南](https://packaging.python.org/)