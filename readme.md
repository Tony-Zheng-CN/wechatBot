# WeChatBot – English Readme

A WeChat bot project that integrates an AI assistant, text-to-speech, image generation, and more.  
<small><small><small><small><small>~~Although I treat her as my little sister :)~~</small></small></small></small></small>

## Project Overview

WeChatBot is a Python-based WeChat robot that offers:

- AI chat assistant (Ollama)  
- Text-to-Speech via ChatTTS & EdgeTTS  
- Image generation via Stable Diffusion API  
- Graphical User Interface (GUI)  
- Bing search integration  
- Long-term memory management  
- User-management system  

Its goal is to provide an intelligent WeChat bot capable of natural conversation, command execution, image creation, and more.

## Features

### AI Chat Assistant
- Customizable persona settings  
- Long-term memory management  
- Bing search for up-to-date information  
- Multimodal support (if the model allows)

### Text-to-Speech
- TTS services included

### Image Generation
- Stable Diffusion API integration  
- Prompt-based image creation

### User Management
- GUI-based user addition  
- Profile and configuration management

### Other
- Global hotkey (Ctrl+Shift+Alt+Esc) to force-quit  
- Configurable cache & model paths  
- Logging and debugging

## Changelog

| Version | Highlights | Date |
|---------|------------|------|
| v1.0.0  | Initial release | 2025-08-27 |
| v1.0.1  | Modularized core modules<br/>GUI now uses ttkbootstrap<br/>Added OpenAI API adapter | 2025-08-28 |

## Directory Layout

```
├── ai_agent/            # AI-related modules  
│   ├── bing_crawler.py  # Bing search crawler  
│   ├── fastchat_ver.py  # FastChat AI agent (deprecated)  
│   ├── memory_manger.py # Memory manager  
│   ├── ollama_ver.py    # Ollama AI agent  
│   ├── api_ver.py       # API-style AI agent  
│   ├── sd_api.py        # Stable Diffusion API interface  
│   ├── tts.py           # Text-to-speech interface  
│   └── system_format.txt# Default configuration  
├── resources/           # Static assets  
│   ├── icon.txt         # App icon (customizable)  
│   ├── command_help_wechat.txt # In-chat help  
│   └── help.txt         # CLI help  
├── l2d_agent/           # Live2D module  
│   └── l2d_control.py   # Live2D avatar control  
├── set/                 # User settings  
├── cache/               # Temporary files  
├── memories/            # Persistent memory  
├── add_user.py          # Add-user utility  
├── config.json          # Main configuration  
├── config_manager.py    # Config loader/saver  
├── gui.py               # GUI entry point  
├── gui_control.py       # GUI-to-WeChat bridge  
├── core.py              # Core engine  
└── main.py              # CLI entry point
```

## Installation & Setup

### Requirements
- Python 3.10+  
- Dependencies listed in `requirements.txt`  
- WeChat PC **v3.x** (v4.x not yet supported)  
- Optional:  
  - Stable Diffusion endpoint  
  - ChatTTS

### Steps
1. Clone the repo  
2. Install deps: `pip install -r requirements.txt`  
3. Configure external services (Ollama, Stable Diffusion, etc.)  
4. Launch: `python main.py` (TUI) or `python gui.py` (GUI)

### Configuration
- `config.json` – main settings (cache paths, model choices…)  
- `set/` – per-user overrides  
- `tts_config.json` – TTS settings

## Usage

### Launching
- CLI/TUI: `python main.py`  
- GUI: `python gui.py` or type `gui` in TUI

### Hotkey
- `Ctrl+Shift+Alt+Esc` – force shutdown

### GUI
A full GUI is provided for user management and configuration tweaks.

## Key Modules

### AI Agent (`ai_agent/`)
Handles all AI interactions:

- `ollama_ver.py` – Ollama backend  
- `fastchat_ver.py` – FastChat backend (deprecated)  
- `api_ver.py` – Generic API backend  
- `sd_api.py` – Stable Diffusion wrapper  
- `memory_manger.py` – Conversation memory  
- `bing_crawler.py` – Web search

### GUI (`gui.py`, `gui_control.py`)
Tkinter/ttkbootstrap-based interface with live WeChat control.

### Configuration (`config_manager.py`, `config.json`)
JSON-based, hot-reloadable settings.

## Development & Contributing
Issues and PRs are welcome.

## Roadmap

| Feature | Target Version | ETA |
|---------|----------------|-----|
| Support for newer WeChat | v1.0.3 | 2025-09 |
| Live2D video calls | v1.1 | 2025-09 |
| Group chat / multi-user | v1.2 | 2025-10 |

<small>Timelines are estimates.</small>

## License

MIT

## Contact

zhengyifantony@outlook.com  
[一只信息课代表 @ Bilibili](https://space.bilibili.com/1969540992)  
<small><small><small><small><small><small><small><small><small><small><small><small><small><small><small><small><small><small><small>[Something Interesting](resources/game/game.py)</small></small></small></small></small></small></small></small></small></small></small></small></small></small></small></small></small></small></small>