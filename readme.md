# WeChatBot - WeChat Robot

A feature-rich WeChat robot project integrating AI assistant, text-to-speech, image generation and more.

## Project Introduction

WeChatBot is a Python-based WeChat robot project with the following main features:

- AI chat assistant (supporting Ollama and FastChat)
- Text-to-speech (TTS) functionality
- Image generation capabilities (via Stable Diffusion API)
- Graphical user interface (GUI)
- Bing search integration
- Memory management functionality
- User management system

This project aims to provide an intelligent WeChat robot solution that can engage in natural conversations, execute commands, generate images, and more.

## Features

### AI Chat Assistant
- Integration with multiple AI models (Ollama and FastChat)
- Support for personalized character settings
- Long-term memory management
- Bing search integration for up-to-date information

### Text-to-Speech
- Built-in TTS service
- Support for various voice configuration options

### Image Generation
- Integration with Stable Diffusion API
- Support for text prompt-based image generation

### User Management
- Graphical user addition interface
- User information configuration management

### Other Features
- Hotkey support (Ctrl+Shift+Alt+Esc)
- Configurable cache paths and model settings
- Logging and debugging functionality

## Directory Structure
├── ai_agent/ # AI agent related modules 
│ ├── bing_crawler.py # Bing search crawler 
│ ├── fastchat_ver.py # FastChat version AI agent 
│ ├── memory_manger.py # Memory manager 
│ ├── ollama_ver.py # Ollama version AI agent 
│ ├── sd_api.py # Stable Diffusion API interface 
│ ├── tts.py # Text-to-speech service 
│ └── system_format.txt # Default configuration 
├── resources/ # Resource files 
│ └── help.txt # Help documentation 
├── set/ # User settings directory 
├── draw/ # Drawing output directory 
├── cache/ # Cache directory 
├── memories/ # Memory storage directory 
├── add_user.py # User addition functionality 
├── config.json # Main configuration file 
├── config_manager.py # Configuration manager 
├── gui.py # Graphical user interface 
├── gui_control.py # GUI control logic 
└── main.py # Main program entry
## Installation and Configuration

### Requirements
- Python 3.7+
- Required packages (defined in requirements.txt)
- WeChat PC version **V3.x** (4.x not yet supported)
- Optional:
  - Stable Diffusion
  - ChatTTS

### Installation Steps
1. Clone the project locally
2. Install dependencies: `pip install -r requirements.txt`
3. Configure related services (such as Ollama, Stable Diffusion, etc.)
4. Run the main program: `python main.py`

### Configuration
- `config.json`: Main configuration file containing cache paths, model selection and other settings
- `set/` directory: Stores user personalization setting files
- `tts_config.json`: Text-to-speech configuration file

## Usage

### Starting the Program
Run `python main.py` to start the program. The program will load configurations and initialize the AI agent.

### Hotkey
- `Ctrl+Shift+Alt+Esc`: Force stop the robot

### Supported Commands
- `/help`: Display help information
- `/exit`: Exit the program
- `/tts`: Toggle text-to-speech functionality
- `/model`: Model management
- `#draw [prompt]`: Generate image based on prompt

### Graphical Interface
The program provides a graphical user interface for user management, configuration adjustments and other operations.

## Main Module Descriptions

### AI Agent Modules (ai_agent/)
Implements interaction functionality with AI models, supporting multiple model backends:
- [ollama_ver.py](file://D:\Workspace_Tony\Data\projects\python\wechatbot\ai_agent\ollama_ver.py): Ollama model interface
- ~~[fastchat_ver.py](file://D:\Workspace_Tony\Data\projects\python\wechatbot\ai_agent\fastchat_ver.py): FastChat model interface~~
- [memory_manger.py](file://D:\Workspace_Tony\Data\projects\python\wechatbot\ai_agent\memory_manger.py): Memory management functionality
- [bing_crawler.py](file://D:\Workspace_Tony\Data\projects\python\wechatbot\ai_agent\bing_crawler.py): Web search functionality

### GUI Modules
- [gui.py](file://D:\Workspace_Tony\Data\projects\python\wechatbot\gui.py): Graphical interface implementation
- [gui_control.py](file://D:\Workspace_Tony\Data\projects\python\wechatbot\gui_control.py): Interface control logic

### Configuration Management
- [config_manager.py](file://D:\Workspace_Tony\Data\projects\python\wechatbot\config_manager.py): Configuration file read/write
- [config.json](file://D:\Workspace_Tony\Data\projects\python\wechatbot\config.json): Main configuration file

## Development and Contributions

Issues and Pull Requests are welcome to improve the project.

## License

[License information to be added]

## Contact

[Contact information to be added]
