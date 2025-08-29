# WeChatBot 每 English Readme

A WeChat bot project that integrates an AI assistant, text-to-speech, image generation, and more.  

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
念岸岸 ai_agent/            # AI-related modules  
岫   念岸岸 bing_crawler.py  # Bing search crawler  
岫   念岸岸 fastchat_ver.py  # FastChat AI agent (deprecated)  
岫   念岸岸 memory_manger.py # Memory manager  
岫   念岸岸 ollama_ver.py    # Ollama AI agent  
岫   念岸岸 api_ver.py       # API-style AI agent  
岫   念岸岸 sd_api.py        # Stable Diffusion API interface  
岫   念岸岸 tts.py           # Text-to-speech interface  
岫   弩岸岸 system_format.txt# Default configuration  
念岸岸 resources/           # Static assets  
岫   念岸岸 icon.txt         # App icon (customizable)  
岫   念岸岸 command_help_wechat.txt # In-chat help  
岫   弩岸岸 help.txt         # CLI help  
念岸岸 l2d_agent/           # Live2D module  
岫   弩岸岸 l2d_control.py   # Live2D avatar control  
念岸岸 set/                 # User settings  
念岸岸 cache/               # Temporary files  
念岸岸 memories/            # Persistent memory  
念岸岸 add_user.py          # Add-user utility  
念岸岸 config.json          # Main configuration  
念岸岸 config_manager.py    # Config loader/saver  
念岸岸 gui.py               # GUI entry point  
念岸岸 gui_control.py       # GUI-to-WeChat bridge  
念岸岸 core.py              # Core engine  
弩岸岸 main.py              # CLI entry point
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
- `config.json` 每 main settings (cache paths, model choices＃)  
- `set/` 每 per-user overrides  
- `tts_config.json` 每 TTS settings

## Usage

### Launching
- CLI/TUI: `python main.py`  
- GUI: `python gui.py` or type `gui` in TUI

### Hotkey
- `Ctrl+Shift+Alt+Esc` 每 force shutdown

### GUI
A full GUI is provided for user management and configuration tweaks.

## Key Modules

### AI Agent (`ai_agent/`)
Handles all AI interactions:

- `ollama_ver.py` 每 Ollama backend  
- `fastchat_ver.py` 每 FastChat backend (deprecated)  
- `api_ver.py` 每 Generic API backend  
- `sd_api.py` 每 Stable Diffusion wrapper  
- `memory_manger.py` 每 Conversation memory  
- `bing_crawler.py` 每 Web search

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
<small><small><small><small><small><small><small><small><small><small><small><small><small><small><small><small><small><small><small>[Something Interesting](resources/game/game.py)</small></small></small></small></small></small></small></small></small></small></small></small></small></small></small></small></small></small></small>
