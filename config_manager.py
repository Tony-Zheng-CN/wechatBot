import json, os, logging

logger = logging.getLogger("config_manager")


def get_config(key):
    try:
        config = json.load(open("config.json", "r", encoding="utf-8"))
    except FileNotFoundError or PermissionError:
        config = {
            "cache": f'{os.getcwd()}\\cache\\',
            "model": "qwen3:0.6b",
            "tts": False,
            "debug": False,
            "launcher": "ollama",
            "draw": False,
            "llm_path": "http://localhost:11434",
            "sd_path": "http://localhost:7860",
        }
    for k, v in config.items():
        if k == key:
            logger.debug(f"Get config success.Key:{k}Value:{v}")
            return v
    logger.debug(f"Get config failed(not found).Key:{key}")
    return None


def save_config(key, value):
    try:
        config = json.load(open("config.json", "r", encoding="utf-8"))
    except FileNotFoundError or PermissionError:
        config = {
            "cache": f'{os.getcwd()}\\cache\\',
            "model": "qwen3:0.6b",
            "tts": False,
            "debug": False,
            "launcher": "ollama",
            "draw": False,
            "llm_path": "http://localhost:11434",
            "sd_path": "http://localhost:7860"
        }
    config[key] = value
    with open("config.json", "w+", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
        logger.info(f"""Save config to{os.path.join(os.getcwd(), "config.json")}""")
