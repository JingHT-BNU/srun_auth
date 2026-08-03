# SrunAuth

[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

一个纯命令行实现的深澜 (Srun) 校园网认证工具，专为无图形界面环境设计。

## 项目简介

`srun_auth` 是一个基于 Python 的深澜校园网登录程序。通常深澜认证需要通过浏览器访问网页并输入账号密码，这对于没有桌面环境的设备（如服务器、树莓派或纯命令行 Linux）非常不友好。

本项目通过爬虫技术模拟了浏览器的认证请求，实现了**纯命令行一键登录**，让你的无头设备也能轻松接入校园网。理论上支持所有使用深澜认证系统的高校。

## 特性

-   **纯命令行操作**：无需 GUI，完美适配 SSH 远程管理场景
-   **交互式配置**：首次运行自动生成配置文件，后续支持手动编辑
-   **通用性强**：适用于绝大多数深澜认证网关
-   **Python 实现**：跨平台，依赖轻量

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/JingHT-BNU/srun_auth.git
cd srun_auth
```

### 2. 安装依赖

确保你的环境中已安装 Python 3.x，然后安装所需库：

```bash
pip install -r requirements.txt
```

### 3. 生成配置

首次使用需运行配置生成脚本，根据终端提示输入你的校园网账号、密码及认证地址等信息：

```bash
python generate_config.py
```

> 💡 **提示**：配置完成后会在当前目录生成 `config.py` 文件。如需修改参数，可直接编辑该文件，无需重新运行生成脚本。

### 4. 执行认证

```bash
python srun_auth.py
```

看到认证成功提示后，即可正常访问网络。

## 开发中功能

### 自动网络检测 (`detect_connection.py`)

目前项目中包含一个尚未完成的 `detect_connection.py` 脚本。

-   **目标**：自动识别当前设备是通过有线还是无线方式连接网络。
-   **用途**：解决部分高校有线网络和无线网络认证入口 URL 不一致的问题，实现全自动切换认证地址。
-   **状态**：WIP (Work In Progress)，欢迎贡献代码！

## 许可证

本项目采用 **WTFPL** (Do What The F*ck You Want To Do Public License) 开源。

你可以对这段代码做任何你想做的事。详情请参阅 [LICENSE](LICENSE) 文件或访问 [WTFPL 官网](http://www.wtfpl.net/)。

## 免责声明

-   本工具仅供学习与研究网络认证机制使用。
-   请遵守所在学校的校园网使用管理规定，切勿利用本工具进行违规共享网络或攻击认证服务器等行为。
-   因使用本工具产生的一切后果由使用者自行承担。

## 贡献

如果你发现 Bug、有新的适配需求或想完善 `detect_connection.py`，欢迎提交 Issue 或 Pull Request！
