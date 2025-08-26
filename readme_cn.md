# WeChatBot - 微信机器人

一个微信机器人项目，集成了AI助手、文本转语音、图像生成等功能。  
<small><small><small><small><small>~~虽然我是当成妹妹的:)~~</small></small></small>

## 项目简介

WeChatBot是一个基于Python开发的微信机器人项目，具备以下主要功能：

- AI聊天助手（Ollama）
- 文本转语音(TTS)功能(ChatTTS&EdgeTTS)
- 图像生成能力（通过Stable Diffusion API）
- 图形用户界面(GUI)
- Bing搜索集成
- 记忆管理功能
- 用户管理系统

该项目旨在提供一个智能化的微信机器人解决方案，可以进行自然对话、执行命令、生成图像等操作。

## 功能特性

### AI聊天助手
- 支持个性化角色设定
- 具备长期记忆管理
- 集成Bing搜索功能以获取最新信息

### 文本转语音
- 内置TTS服务
- 支持多种语音配置选项

### 图像生成
- 集成Stable Diffusion API
- 支持文本提示生成图像

### 用户管理
- 图形化用户添加界面
- 用户信息配置管理

### 其他功能
- 快捷键支持（Ctrl+Shift+Alt+Esc）
- 可配置的缓存路径和模型设置
- 日志记录和调试功能

## 目录结构
    ├── ai_agent/ # AI代理相关模块 
    │ ├── bing_crawler.py # Bing搜索爬虫 
    │ ├── fastchat_ver.py # FastChat版本AI代理 
    │ ├── memory_manger.py # 记忆管理器 
    │ ├── ollama_ver.py # Ollama版本AI代理 
    │ ├── sd_api.py # Stable Diffusion API接口 
    │ ├── tts.py # 文本转语音服务 
    │ └── system_format.txt # 默认配置
    ├── resources/ # 资源文件 
    │ └── help.txt # 帮助文档 
    ├── set/ # 用户设定目录 
    ├── draw/ # 绘图输出目录
    ├── cache/ # 缓存目录 
    ├── memories/ # 记忆存储目录 
    ├── add_user.py # 用户添加功能 
    ├── config.json # 主配置文件 
    ├── config_manager.py # 配置管理器 
    ├── gui.py # 图形用户界面 
    ├── gui_control.py # GUI控制逻辑 
    └── main.py # 主程序入口

## 安装与配置

### 环境要求
- Python 3.7+
- 相关依赖包（在requirements.txt中定义）
- 微信PC版 **V3.x** (4.x暂未支持)
- 可选:
  - Stable Diffusion
  - ChatTTS

### 安装步骤
1. 克隆项目到本地
2. 安装依赖包：`pip install -r requirements.txt`
3. 配置相关服务（如Ollama、Stable Diffusion等）
4. 运行主程序：`python main.py`

### 配置说明
- `config.json`：主配置文件，包含缓存路径、模型选择等设置
- `set/`目录：存放用户个性化设置文件
- `tts_config.json`：文本转语音配置文件

## 使用方法

### 启动程序
运行`python main.py`启动程序，程序将加载配置并初始化AI代理。

### 快捷键
- `Ctrl+Shift+Alt+Esc`：强制关闭机器人

### 命令支持
- `/help`：显示帮助信息
- `/exit`：退出程序
- `/tts`：文本转语音功能
- `/model`：模型管理
- `#draw [prompt]`：根据提示生成图像

### 图形界面
程序提供图形用户界面，可通过界面进行用户管理、配置调整等操作。

## 主要模块说明

### AI代理模块 (ai_agent/)
实现了与AI模型的交互功能，支持多种模型后端：
- [ollama_ver.py](file://D:\Workspace_Tony\Data\projects\python\wechatbot\ai_agent\ollama_ver.py)：Ollama模型接口
- ~~[fastchat_ver.py](file://D:\Workspace_Tony\Data\projects\python\wechatbot\ai_agent\fastchat_ver.py)：FastChat模型接口~~
- [memory_manger.py](file://D:\Workspace_Tony\Data\projects\python\wechatbot\ai_agent\memory_manger.py)：记忆管理功能
- [bing_crawler.py](file://D:\Workspace_Tony\Data\projects\python\wechatbot\ai_agent\bing_crawler.py)：网络搜索功能

### GUI模块
- [gui.py](file://D:\Workspace_Tony\Data\projects\python\wechatbot\gui.py)：图形界面实现
- [gui_control.py](file://D:\Workspace_Tony\Data\projects\python\wechatbot\gui_control.py)：微信界面控制逻辑

### 配置管理
- [config_manager.py](file://D:\Workspace_Tony\Data\projects\python\wechatbot\config_manager.py)：配置文件读写
- [config.json](file://D:\Workspace_Tony\Data\projects\python\wechatbot\config.json)：主配置文件

## 开发与贡献

欢迎提交Issue和Pull Request来改进项目。

## 许可证

[待添加许可证信息]

## 联系方式

zhengyifantony@outlook.com  
[一只信息课代表@bilibili](https://space.bilibili.com/1969540992)
<small><small><small><small><small><small><small><small><small><small><small><small><small><small><small><small>[奇妙小作文](resources/text/1.txt)</small></small></small></small></small></small></small></small></small></small></small></small></small></small></small></small>