# CI/CD 配置说明

本项目使用 GitHub Actions 实现自动化测试和发布流程。

## 工作流概述

### 1. CI (持续集成) - `ci.yml`

在以下情况触发：
- 推送到 `main`, `master`, `develop` 分支
- 创建 Pull Request

执行内容：
- 多平台测试 (Ubuntu, Windows, macOS)
- 多 Python 版本测试 (3.7-3.11)
- 代码风格检查 (flake8, black)
- 类型检查 (mypy)
- 安全检查 (bandit)
- 构建检查

### 2. 发布到 PyPI - `publish.yml`

在以下情况触发：
- 推送标签 (格式: `v*`, 如 `v1.0.0`)
- 手动触发 (用于测试)

执行流程：
1. 运行测试
2. 构建包
3. 发布到 PyPI (标签触发) 或 Test PyPI (手动触发)
4. 创建 GitHub Release

### 3. Release Drafter - `release-drafter.yml`

自动生成发布说明草稿，根据 PR 标签分类变更内容。

## 设置步骤

### 1. 配置 PyPI 发布权限

使用 Trusted Publishers (推荐):

1. 登录 [PyPI](https://pypi.org)
2. 进入项目设置
3. 添加 GitHub 发布者:
   - Owner: `twwch`
   - Repository: `bilibili-downloader`
   - Workflow: `publish.yml`
   - Environment: `pypi`

### 2. 配置 GitHub Secrets (备选方案)

如果不使用 Trusted Publishers，需要配置：
- `PYPI_API_TOKEN`: PyPI API token
- `TEST_PYPI_API_TOKEN`: Test PyPI API token

### 3. 配置 GitHub Environment

创建名为 `pypi` 的 environment，用于发布保护。

## 发布新版本

### 自动发布流程

1. 更新版本号：
   ```bash
   python scripts/release.py 1.0.1
   ```

2. 推送代码和标签：
   ```bash
   git push
   git push --tags
   ```

3. GitHub Actions 自动：
   - 运行测试
   - 构建包
   - 发布到 PyPI
   - 创建 GitHub Release

### 手动发布流程

1. 更新版本号：
   ```bash
   # 修改以下文件中的版本号
   # - bilibili_downloader/__init__.py
   # - setup.py
   # - pyproject.toml
   ```

2. 提交并打标签：
   ```bash
   git add -A
   git commit -m "Bump version to 1.0.1"
   git tag -a v1.0.1 -m "Release version 1.0.1"
   ```

3. 推送触发发布：
   ```bash
   git push origin main
   git push origin v1.0.1
   ```

## 测试发布

1. 在 Actions 页面手动触发 `Publish to PyPI` 工作流
2. 选择要测试的分支
3. 包会发布到 Test PyPI

测试安装：
```bash
pip install -i https://test.pypi.org/simple/ bilibili-downloader
```

## 常见问题

### 1. 发布失败：权限错误

确保已正确配置 Trusted Publishers 或 API Token。

### 2. 测试失败

- 检查测试日志
- 本地运行测试：`pytest`
- 确保所有依赖已安装

### 3. 版本冲突

确保版本号在所有文件中一致：
- `bilibili_downloader/__init__.py`
- `setup.py`  
- `pyproject.toml`

## 维护建议

1. **版本管理**：遵循语义化版本 (SemVer)
2. **测试覆盖**：保持高测试覆盖率
3. **文档更新**：发布前更新 CHANGELOG.md
4. **依赖更新**：定期更新依赖 (Dependabot 自动创建 PR)

## 相关链接

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [语义化版本](https://semver.org/lang/zh-CN/)