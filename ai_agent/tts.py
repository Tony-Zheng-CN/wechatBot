import asyncio
import hashlib
import json
import os
import random
import string
import time
import urllib.request as urlr
import requests
import shutil
import edge_tts


def get_tts_config():
    try:
        config = json.load(open("tts_config.json", "r", encoding="utf-8"))
    except FileNotFoundError or PermissionError:
        config = {}
    app_id = config.get("id", "")
    key = config.get("key", "")
    return app_id, key

def _chattts(tts_path, reply, cache_path="cache"):
    try:
        res = requests.post(tts_path, data={
            "text": reply,
            "prompt": "",
            "voice": "3333",
            "temperature": 0.3,
            "top_p": 0.7,
            "top_k": 20,
            "skip_refine": 0,
            "custom_voice": 0
        })
        file_path = os.path.join(cache_path, f"tts_{time.time()}.mp3")
        shutil.copy(res.json()["file_name"], file_path)
        return file_path
    except requests.exceptions.JSONDecodeError as e:
        print(f"Failed to decode JSON response from TTS service: {e}")
    except Exception as e:
        print(f"[Error]Error occurred while sending TTS request: {e}")

def _xdf(app_id, app_sec, reply, cache_path="cache", volume=1.0, speed=1.0, lang="ch"):
    host = 'https://gate.ai.xdf.cn/'
    param = json.dumps({'text': reply, 'lang': lang, 'msgid': '003', 'speed': speed, 'volume': volume})
    timestamp = time.time()
    timestamp = str(round(timestamp * 1000))
    salt = ''.join(random.sample(string.ascii_letters, 8))
    sign = app_id + app_sec + salt + timestamp
    sign = hashlib.md5(sign.encode(encoding='UTF-8')).hexdigest()

    headers = {'Content-Type': 'application/json', 'app_id': app_id, 'timestamp': timestamp, 'salt': salt, 'sign': sign}
    url = f"{host}/offline/{lang}_tts/v1"
    r = requests.post(url, data=param, headers=headers)
    try:
        if r.json()["result"]["audio"] is None:
            return False
        file_web = r.json()["result"]["audio"]
        file_path = os.path.join(cache_path, f"tts_{time.time()}.mp3")
        file = open(file_path, "wb+")
        response = requests.get(file_web)
        if response.status_code == 200:
            file.write(response.content)
        return file_path
    except Exception as e:
        return e,r.text


def _edgetts(reply, cache_path):
    VOICE = "zh-CN-YunyangNeural"

    async def _async_tts():
        communicate = edge_tts.Communicate(reply, VOICE)
        file_path = os.path.join(cache_path, f"tts_{time.time()}.mp3")
        await communicate.save(file_path)
        return file_path

    # 使用 asyncio.run() 运行异步函数
    return asyncio.run(_async_tts())

def tts_service(reply, cache_path="", tts_path=None, type="edge"):
    match type:
        case "local":
            return _chattts(tts_path, reply, cache_path)
        case "xdf":
            app_id, key = get_tts_config()
            return _xdf(app_id, key, reply, cache_path)
        case "edge":
            return _edgetts(reply, cache_path)
        case _:
            return False

if __name__ == '__main__':
    print(tts_service("TTS 测试", type="edge"))