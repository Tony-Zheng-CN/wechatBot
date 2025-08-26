# -*- coding: utf-8 -*-
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import threading
import random
from pynput import keyboard

from add_user import add_user
from ai_agent.fastchat_ver import AIAgent as fcAIAgent
from ai_agent.fastchat_ver import model_list as fcML
from ai_agent.ollama_ver import AIAgent as olAIAgent
from ai_agent.ollama_ver import model_list as olML
from ai_agent.sd_api import sd_api_t2i
from ai_agent.tts import tts_service
from config_manager import get_config, save_config
from gui_control import *


logger = logging.getLogger("main")
logger_formatter = logging.Formatter("[%(levelname)s][%(name)s]%(message)s")

help_text = open(os.path.join(os.getcwd(), "resources", "help.txt"), "r", encoding="utf-8").read()
logger.debug(f"""Load help text from{os.path.join(os.getcwd(), "resources", "help.txt")}""")

global cache_path, model, tts, debug, launcher, enable_draw, llm_path, sd_path, l2d_model
cache_path = get_config("cache")
model = get_config("model")
tts = get_config("tts")
debug = get_config("debug")
launcher = get_config("launcher")
llm_path = get_config("llm_path")
sd_path = get_config("sd_path")
enable_draw = get_config("draw")
l2d_model = get_config("l2d_model")
logger.info(f"""Load config from{os.path.join(os.getcwd(), "config.json")}""")

set_debug_gc(debug)

if debug:
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s][%(name)s]%(message)s")
else:
    logging.basicConfig(level=logging.ERROR, format="[%(levelname)s][%(name)s]%(message)s")

set_cache_dir(cache_path)
logger.debug(f"""Load cache dir from{cache_dir}""")

tts_path = 'http://127.0.0.1:9966/tts'

logger.debug(f"""Load sd_api from {sd_path}""")
logger.debug(f"""Load tts from {tts_path}""")

call_times = 0
stop_flag = False
ai_agent = None  # 鍏ㄥ眬 AI 瀹炰緥


def on_press(key):
    if (
            key == keyboard.Key.esc and
            keyboard.Controller().pressed(keyboard.Key.ctrl_l) and
            keyboard.Controller().pressed(keyboard.Key.shift_l) and
            keyboard.Controller().pressed(keyboard.Key.alt_l)
    ):
        global stop_flag
        stop_flag = True
        logging.warning("Main stoped.By hot key")
        print("正在中止程序...")
        return False  # 鍋滄鐩戝惉鍣�


def check_cache():
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)


def wechat_exit():
    try:
        wechat_relog_img = pag.locateCenterOnScreen(os.path.join(os.getcwd(), "resources", "images", "wechat_relogin.png"), confidence=0.8)
        logger.error(f"Wechat exited")
        return True
    except pag.ImageNotFoundException:
        return False

def message_process(reply):
    global call_times
    if not ai_agent:
        return
    if enable_draw:
        if "你要看" and "画" in reply:
            try:
                sd_prompt = ai_agent.get_response(
                    f"从{reply}中提取适用于SD的AI绘画提示词，英语，具体，500词以内。只有单词或短语",
                    memory=False)
                send_message("正在绘画...")
                if debug:
                    logger.debug(f"SD api draw.prompt: {sd_prompt}")
                sd_image_path = sd_api_t2i(sd_prompt, sd_path)
                send_file(sd_image_path)
                time.sleep(0.2)
            except Exception as e:
                send_message("绘画失败")
                logger.error(f"SD api error: {e}")
    if "//call video" in reply:
        reply = reply.replace("//call video", "")
        if call_times <= 0:
            call_video()
            if debug:
                logger.debug(f"Call video.")
                call_times += 1
            else:
                call_times -= 0.1
            time.sleep(0.2)
    if "//touch_head" in reply:
        if debug:
            reply = reply.replace("//touch_head", "")
            head_shot()
            time.sleep(0.2)
    if tts:
        try:
            if debug:
                logger.debug(f"TTS start.")
            send_message("TTS...")
            tts_dir = tts_service(tts_path, reply, cache_path)
            if debug:
                logger.debug(f"TTS complete.File:{tts_dir}")
            if tts_dir:
                send_file(tts_dir)
        except Exception as e:
            if debug:
                logger.error(f"TTS error: {e}")
            send_message("哥哥！是不是你把我的声带偷了！！！：" + str(e))
    send_message(reply)


def start():
    global enable_draw, cache_path, model, tts, debug, launcher, ai_agent, call_times
    activate_wechat_window()
    check_cache()
    place = click_user()
    logger.debug(f"Main started")
    logger.info(f"LLM模型:{model}\n运行器:{launcher}")
    if place:
        if debug:
            send_message(f"[DEBUG]{model}已接入")
        click_user_next()
        if launcher == "fastchat":
            ai_agent = fcAIAgent(user_name=user)  # 鍒濆鍖� AI
        elif launcher == "ollama":
            ai_agent = olAIAgent(user_name=user, model=model, host=llm_path)
        listener_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=on_press).start())
        listener_thread.start()
        last_chat_time = time.time()
        chat_delay = random.randint(300, 3600)
        logger.info(f"Auto chat delay:{chat_delay}")
        while not stop_flag or wechat_exit():
            place = check_unread_message()
            if place:
                pag.click(x=place[0] + 30, y=place[1] + 20)
                new_message = get_new_message()
                if not new_message[1]:
                    continue
                message_type = new_message[0]
                if debug:
                    logger.info(f"New message:{new_message}")
                if new_message[0]:
                    if new_message[0] == "text":
                        new_message = new_message[1]
                        if new_message.startswith("#"):
                            if new_message.split(" ")[0] == "#call":
                                type_text = new_message.split(" ")[1]
                                if type_text == "sound":
                                    call_sound()
                                elif type_text == "video":
                                    call_video()
                            elif new_message.split(" ")[0] == "#open":
                                type_text = new_message.split(" ")[1]
                                message_text = new_message.split(" ")[2]
                                if type_text == "web":
                                    send_message(f"已经在哥哥的电脑上打开：{message_text}")
                                    open_web(message_text)
                            elif new_message.split(" ")[0] == "#draw":
                                send_message("正在绘画...")
                                send_file(sd_api_t2i(new_message.split(" ")[1], sd_path))
                                if debug:
                                    logger.debug(f"Sd draw.prompt{new_message.split(' ')[1]}")
                            elif new_message.split(" ")[0] == "#fadian":
                                for i in range(random.randint(1, 1000)):
                                    send_message(f"{random.randint(1, 10000)}")
                            click_user_next()
                            continue
                        elif new_message.startswith("/"):
                            if new_message.split(" ")[0] == "/exit":
                                logger.warning("Main exit.By wechat ")
                                exit()
                            elif new_message.split(" ")[0] == "/help":
                                send_message(help_text)
                                logger.debug("Print help_text")
                            elif new_message.split(" ")[0] == "/tts":
                                if tts:
                                    tts = False
                                else:
                                    tts = True
                                if debug:
                                    send_message(f"TTS:{tts}")
                                    logger.info(f"TTS change to {tts}")
                                save_config("tts", tts)
                            elif new_message.split(" ")[0] == "/tts_status":
                                send_message(f"TTS:{tts}")
                                if debug:
                                    logger.info(f"Ask for TTS:{tts}")
                            elif new_message.split(" ")[0] == "/debug":
                                if debug:
                                    debug = False
                                else:
                                    debug = True
                                if debug:
                                    send_message(f"debug:{debug}")
                                    logger.info(f"Debug change to {debug}")
                                save_config("debug", debug)
                            elif new_message.split(" ")[0] == "/shutdown":
                                send_message("哥哥你的电脑报废了...")
                                logger.info("Shutdown.By wechat")
                                import os
                                os.system("shutdown -s -t 0")
                            elif new_message.split(" ")[0] == "/file":
                                try:
                                    message_text = new_message.split(" ")[1]
                                except IndexError:
                                    message_text = ""
                                if debug:
                                    send_message("正在发送文件...")
                                    logger.info(f"Send file from {message_text}")
                                send_file(message_text)
                            elif new_message.startswith("/dir"):
                                try:
                                    message_text = new_message.split(" ")[1]
                                except IndexError:
                                    message_text = ""
                                if debug:
                                    send_message("正在发送文件夹目录...")
                                    logger.info(f"Send dir index from {message_text}")
                                send_dir(message_text)
                            elif new_message == "/reset":
                                os.remove(f"memories\\{user}.txt")
                                if debug:
                                    send_message("记忆已重置")
                                    logger.info(f"Memory clear({user}).By wechat")
                            elif new_message.split(" ")[0] == "/model":
                                if launcher == "ollama":
                                    model_list = olML(llm_path)
                                else:
                                    model_list = fcML()
                                if new_message.split(" ")[1] == "list":
                                    logger.debug(f"Get model list({model_list}).By wechat")
                                    send_message(str(model_list))
                                elif new_message.split(" ")[1] == "set":
                                    new_model = new_message.split(" ")[2]
                                    if new_model in model_list:
                                        model = new_model
                                        send_message(f"已切换LLM模型为{model}")
                                        save_config("model", model)
                                        logger.debug(f"Model change to {model}.By wechat")
                                    else:
                                        send_message(f"无名为{new_model}的LLM模型")
                                        logger.warning(f"Model not found.{new_model}.By wechat")
                                else:
                                    send_message(f"无名为{new_message}的指令")
                                    logger.warning(f"Command not found.{new_message}.By wechat")
                            click_user_next()
                            continue
                        send_message("少女思考中...")
                        logger.debug(f"Get response from {model}")
                        result = {}
                        try:
                            result['response'] = ai_agent.get_response((message_type, new_message))
                        except Exception as e:
                            result['response'] = "呜呜~思考过程中断了啦！"
                            logger.error(f"AI response error: {e}")

                        reply = result.get('response', "呜呜~我没有想好要说什么...")
                        message_process(reply)
                        time.sleep(0.2)
                        call_times -= 0.1
                    click_user_next()
                    last_chat_time = time.time()
                    chat_delay = random.randint(300, 3600)
            elif time.time() - last_chat_time >= chat_delay:
                logger.info(f"Auto send Message.(wait time:{chat_delay})")
                click_user()
                reply = ai_agent.get_response(("auto", chat_delay))
                logger.info(f"Auto message:{reply}")
                message_process(reply)
                last_chat_time = time.time()
                chat_delay = random.randint(300, 3600)
        if wechat_exit():
            logger.critical("Wechat Exit.Main Stopped")
        else:
            send_message("用户中止")
            logger.info("Main Stopped by user")
    else:
        print(f"无法在列表中找到{user}。中止")
        logger.error(f"User not found.{user}")


if __name__ == "__main__":
    os.system("cls")
    if get_config("user"):
        user = get_config("user")
    else:
        user = ""
    command = ""
    while True:
        if debug:
            print("因为Debug已开启，不输出标题")
        else:
            print(open(os.path.join("resources", "icon.txt"), encoding="utf-8").read())
        print(f"当前用户：{user}     运行器：{launcher}     LLM模型：{model}      Live2d模型：{l2d_model}\n"
              f"TTS状态：{tts}    缓存路径：{cache_path}     调试模式：{debug}\n")
        cmd_txt = open(os.path.join("resources", "command_help.txt"), encoding="utf-8").read()
        command = input(
            "输入help显示帮助文档\n"
            "请输入命令：")
        command_txt = command
        command = command.split(" ")
        try:
            match command[0]:
                case "restart":
                    os.system("python main.py")
                case "exit":
                    exit()
                case "run":
                    if user == "":
                        print("请先设置用户")
                    else:
                        set_name(user)
                        save_config("user", user)
                        stop_flag = False
                        time.sleep(2)
                        start()
                case "gui":
                    os.system("python gui.py")
                case "help":
                    print(cmd_txt)
                case "user":
                    match command[1]:
                        case "set":
                            user_ = user
                            user = input("请输入用户名：")
                            if set_name(user):
                                print(f"已切换用户为{user}")
                                user_ = user
                                save_config("user", user)
                            else:
                                user = user_
                                print("用户不存在")
                        case "add":
                            user = input("请输入用户名：")
                            add_user(user)
                        case "mp":
                            if user == "":
                                print("请先设置用户")
                            elif not os.path.exists(f"memories\\{user}.txt"):
                                print("当前用户没有长期记忆")
                            else:
                                print(open(f"memories\\{user}.txt", "r", encoding="utf-8").read())
                        case "mc":
                            if user == "":
                                print("请先设置用户")
                            elif not os.path.exists(f"memories\\{user}.txt"):
                                print("当前用户没有长期记忆")
                            else:
                                if input("确定要删除所有记忆吗？(y/n)") == "y":
                                    os.remove(f"memories\\{user}.txt")
                                    print("记忆已删除")
                                else:
                                    print("取消删除")
                        case "del":
                            if user == "":
                                print("请先设置用户")
                            elif not os.path.exists(
                                    f"set\\{user}.txt") and os.path.exists(f"resources\\images\\{user}"):
                                print(f"用户 {user} 不存在")
                            else:
                                if input("确定要删除用户吗？(y/n)") == "y":
                                    print("已删除用户")
                                    if os.path.exists(os.path.join(os.getcwd(), "memories", f"{user}.txt")):
                                        os.remove(os.path.join(os.getcwd(), "memories", f"{user}.txt"))
                                    os.remove(os.path.join(os.getcwd(), "set", f"{user}.txt"))
                                    shutil.rmtree(os.path.join(os.getcwd(), "resources", "images", user))
                        case "list":
                            user_list = []
                            for user in os.listdir("set"):
                                user_list.append(os.path.splitext(user)[0])
                            print(user_list)
                        case _:
                            print(f"无名为 {command} 的命令")
                case "model":
                    match command[1]:
                        case "set":
                            if launcher == "ollama":
                                model_list = olML(llm_path)
                            else:
                                model_list = fcML()
                            new_model = input("请输入LLM模型名称：")
                            if new_model in model_list:
                                model = new_model
                                print(f"已切换LLM模型为{model}")
                                save_config("model", model)
                            else:
                                print(f"LLM模型 {new_model} 不存在。")
                        case "list":
                            if launcher == "ollama":
                                model_list = olML(llm_path)
                            else:
                                model_list = fcML()
                            print(model_list)
                        case "sr":
                            if input("""运行器("ollama"/"fastchat"):""") in ["ollama", "fastchat"]:
                                launcher = input("""运行器("ollama"/"fastchat"):""")
                            print(f"已切换运行器为{launcher}")
                            save_config("launcher", launcher)
                        case _:
                            print(f"无名为 {command} 的命令")
                case "tts":
                    match command[1]:
                        case "set":
                            tts = not tts
                            print(f"TTS已切换为{tts}")
                            save_config("tts", tts)
                        case _:
                            print(f"无名为 {command} 的命令")
                case "l2d":
                    match command[1]:
                        case "set":
                            input_model = input("请输入Live2D模型名称：")
                            if input_model in os.listdir("l2d_model"):
                                l2d_model = input_model
                                save_config("l2d_model", l2d_model)
                                logging.debug(f"Live2d model set {l2d_model}")
                        case "list":
                            print(os.listdir("l2d_model"))
                            logging.debug(f"Live2d model list {os.listdir('l2d_model')}")
                        case "del":
                            input_model = input("请输入Live2D模型名称：")
                            if os.path.exists(f"l2d_model\\{input_model}"):
                                if input(f"确定要删除Live2D模型 {input_model} 吗？(y/n)") == "y":
                                    shutil.rmtree(f"l2d_model\\{input_model}")
                                    print(f"已删除Live2D模型 {input_model}")
                                    logger.debug(f"Live2D model deleted {input_model}")
                            else:
                                print(f"Live2D模型 {input_model} 不存在。")
                        case "add":
                            input_model = input("请输入Live2D模型文件夹路径：")
                            if os.path.exists(input_model):
                                shutil.copytree(input_model, f"l2d_model\\{os.path.basename(input_model)}")
                                print(f"已添加Live2D模型 {os.path.basename(input_model)}")
                                save_config("l2d_model", os.path.basename(input_model))
                                logger.debug(f"Live2D model added {os.path.basename(input_model)}")
                        case _:
                            print(f"无名为 {command} 的命令")
                case "set":
                    match command[1]:
                        case "debug":
                            debug = not debug
                            print(f"DEBUG已切换为{debug}")
                            save_config("debug", debug)
                        case "cc":
                            clear_cache()
                            input("缓存已清空")
                        case "sc":
                            set_cache_dir(cache_path)
                            cache_dir = input("请输入缓存目录：")
                            save_config("cache", cache_dir)
                        case "tts":
                            tts_path = input("请输入TTS服务器路径：")
                            print(f"已切换TTS服务器为{tts_path}")
                            save_config("tts_path", tts_path)
                            logging.debug(f"TTS path set {tts_path}")
                        case "llm":
                            llm_path = input("请输入LLM服务器路径：")
                            print(f"已切换LLM服务器为{llm_path}")
                            save_config("llm_path", llm_path)
                            logging.debug(f"LLM path set {llm_path}")
                        case "sd":
                            sd_path = input("请输入Stable Diffusion服务器路径：")
                            print(f"已切换Stable Diffusion服务器为{sd_path}")
                            save_config("sd_path", sd_path)
                            logging.debug(f"SD-API path set {sd_path}")
                        case _:
                            print(f"无名为 {command} 的命令")
                case _:
                    print(f"无名为 {command_txt} 的命令")
        except IndexError:
            print("命令不完整")
        input("[请按回车键继续]")
        os.system("cls")
