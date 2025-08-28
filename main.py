import os
import shlex
import subprocess
import sys
import logging
from core import WeChatBot

# === 配置 ===
logger = logging.getLogger("TUI")
core = WeChatBot()
cmd_help = core.get_help()


# 跨平台清屏
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


clear_screen()
title = core.get_title()

# 语言包
lang_cn = {
    "help": "输入help显示帮助文档",
    "success": "执行成功",
    "failed": "执行失败",
    "error": "错误",
    "un_cmd": "未知指令",
    "statue_set": "设为",
    "mem_none": "没有记忆",
    "ask_user_name": "请输入用户名",
    "ask_name": "请输入你的名字",
    "ask_hobby": "请输入你的兴趣爱好",
    "ask_age": "请输入你的年龄",
    "ask_sex": "请输入你的性别",
    "ask_personality": "请输入你的性格",
    "ask_user_background": "请输入你的背景",
    "ask_model_name": "请输入模型名称",
    "ask_model_runner": "请输入模型运行器",
    "ask_model_path": "请输入模型路径",
    "ask_cache_path": "请输入缓存路径",
    "ask_llm_path": "请输入LLM服务器路径",
    "ask_tts_path": "请输入TTS服务器路径",
    "ask_sd_path": "请输入Stable Diffusion服务器路径",
    "press_enter": "[按下回车键继续]",
    "cmd_not_intact": "命令不完整"
}
lang = lang_cn


# 通用异常处理装饰器
def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result:
                print(lang.get("success"))
            else:
                print(lang.get("failed"))
        except Exception as e:
            logger.exception(f"执行失败: {e}")
            print(f"{lang.get('error')}: {e}")

    return wrapper


if __name__ == "__main__":
    while True:
        info = core.get_info()
        print(title)
        print("=== 系统信息 ===")
        for key, value in info.items():
            print(f"{key:>12}: {value}")
        print("================")
        print(lang.get("help"))
        command_text = input("> ").strip()
        command = shlex.split(command_text)

        try:
            match command[0]:
                case "help":
                    print(cmd_help)
                case "restart":
                    os.system("python main.py")
                case "exit":
                    exit()
                case "run":
                    core.core_run()
                case "gui":
                    os.system("python gui.py")
                case "model":
                    match command[1]:
                        case "list":
                            print(core.llm_model_list())
                        case "set":
                            model_name = input(lang.get("ask_model_name"))
                            handle_exception(core.l2d_model_add)(model_name)
                        case "sr":
                            handle_exception(core.llm_model_launcher_set)(input(lang.get("ask_model_runner")))
                        case _:
                            print(f"{lang.get('un_cmd')}: {command_text}")
                case "tts":
                    match command[1]:
                        case "set":
                            print(f"TTS{lang.get('statue_set')}: {core.tts_set()}")
                        case _:
                            print(f"{lang.get('un_cmd')}: {command_text}")
                case "l2d":
                    match command[1]:
                        case "set":
                            model_name = input(lang.get("ask_model_name"))
                            if model_name:
                                handle_exception(core.l2d_model_set)(model_name)
                        case "list":
                            print(core.l2d_model_list())
                        case "del":
                            model_name = input(lang.get("ask_model_name"))
                            if model_name:
                                handle_exception(core.l2d_model_delete)(model_name)
                        case "add":
                            model_path = input(lang.get("ask_model_path"))
                            if model_path:
                                handle_exception(core.l2d_model_add)(model_path)
                        case _:
                            print(f"{lang.get('un_cmd')}: {command_text}")
                case "user":
                    match command[1]:
                        case "set":
                            user = input(lang.get("ask_user_name") + ":")
                            if user:
                                core.user_set(user)
                        case "add":
                            user = input(lang.get("ask_user_name") + ":")
                            name = input(lang.get("ask_name") + ":")
                            age = input(lang.get("ask_age") + ":")
                            sex = input(lang.get("ask_sex") + ":")
                            hobby = input(lang.get("ask_hobby") + ":")
                            personality = input(lang.get("ask_personality") + ":")
                            background = input(lang.get("ask_user_background") + ":")
                            core.user_add({
                                "username": user,
                                "name": name,
                                "age": age,
                                "sex": sex,
                                "hobby": hobby,
                                "personality": personality,
                                "background": background
                            })
                        case "mp":
                            mem = core.user_memory_show()
                            if mem:
                                print(mem)
                            else:
                                print(info.get("user") + lang.get("mem_none"))
                        case "mc":
                            handle_exception(core.user_memory_clear)()
                        case "del":
                            handle_exception(core.user_delete)()
                        case "list":
                            print(core.user_list())
                        case _:
                            print(f"{lang.get('un_cmd')}: {command_text}")
                case "set":
                    match command[1]:
                        case "debug":
                            handle_exception(core.set_debug)()
                        case "tts":
                            path = input(lang.get("ask_tts_path"))
                            if path:
                                handle_exception(core.set_tts_path)(path)
                        case "llm":
                            path = input(lang.get("ask_llm_path"))
                            if path:
                                handle_exception(core.set_llm_path)(path)
                        case "sd":
                            path = input(lang.get("ask_sd_path"))
                            if path:
                                handle_exception(core.set_sd_path)(path)
                        case "cc":
                            handle_exception(core.set_cache_clear)()
                        case "sc":
                            path = input(lang.get("ask_cache_path"))
                            if path:
                                handle_exception(core.set_cache_set)(path)
                        case "draw":
                            handle_exception(core.set_draw)()
                        case _:
                            print(f"{lang.get('un_cmd')}: {command_text}")
                case _:
                    print(f"{lang.get('un_cmd')}: {command_text}")
        except IndexError:
            print(lang.get("cmd_not_intact"))
        input(lang.get("press_enter"))
