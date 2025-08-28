# -*- coding: utf-8 -*-
import threading
import random

from pynput import keyboard

from add_user import NewUser
from ai_agent.fastchat_ver import AIAgent as fcAIAgent
from ai_agent.fastchat_ver import model_list as fcML
from ai_agent.ollama_ver import AIAgent as olAIAgent
from ai_agent.ollama_ver import model_list as olML
from ai_agent.api_ver import AIAgent as oaAIAgent
from ai_agent.api_ver import model_list as oaML
from ai_agent.sd_api import sd_api_t2i
from ai_agent.tts import tts_service
from config_manager import get_config, save_config
from gui_control import *

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


class WeChatBot:
    def __init__(self):
        self.logger = logging.getLogger("core")
        logger_formatter = logging.Formatter("[%(levelname)s][%(name)s]%(message)s")

        self.cache_path = get_config("cache")
        self.model = get_config("model")
        self.tts = get_config("tts")
        self.debug = get_config("debug")
        self.launcher = get_config("launcher")
        self.llm_path = get_config("llm_path")
        self.sd_path = get_config("sd_path")
        self.enable_draw = get_config("draw")
        self.l2d_model = get_config("l2d_model")
        self.logger.info(f"""Load config from{os.path.join(os.getcwd(), "config.json")}""")
        if get_config("user"):
            self.user = get_config("user")
        else:
            self.user = ""

        set_debug_gc(self.debug)

        if self.debug:
            logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s][%(name)s]%(message)s")
        else:
            logging.basicConfig(level=logging.ERROR, format="[%(levelname)s][%(name)s]%(message)s")

        set_cache_dir(self.cache_path)
        self.logger.debug(f"""Load cache dir from{cache_dir}""")

        self.tts_path = 'http://127.0.0.1:9966/tts'

        self.logger.debug(f"""Load sd_api from {self.sd_path}""")
        self.logger.debug(f"""Load tts from {self.tts_path}""")

        self.call_times = 0
        self.stop_flag = False
        self.ai_agent = None

    def on_press(self, key):
        if (
                key == keyboard.Key.esc and
                keyboard.Controller().pressed(keyboard.Key.ctrl_l) and
                keyboard.Controller().pressed(keyboard.Key.shift_l) and
                keyboard.Controller().pressed(keyboard.Key.alt_l)
        ):
            self.stop_flag = True
            logging.info("Main stoped.By hot key")
            return False
        return None

    def check_cache(self):
        if not os.path.exists(self.cache_path):
            os.mkdir(self.cache_path)

    def wechat_exit(self):
        try:
            wechat_relog_img = pag.locateCenterOnScreen(
                os.path.join(os.getcwd(), "resources", "images", "wechat_relogin.png"), confidence=0.8)
            self.logger.error(f"Wechat exited")
            return True
        except pag.ImageNotFoundException:
            return False

    def message_process(self, reply):
        if not self.ai_agent:
            return
        if self.enable_draw:
            if "你要看" and "画" in reply:
                try:
                    sd_prompt = self.ai_agent.get_response(
                        f"从{reply}中提取适用于SD的AI绘画提示词，英语，具体，500词以内。只有单词或短语",
                        memory=False)
                    send_message("正在绘画...")
                    if self.debug:
                        self.logger.debug(f"SD api draw.prompt: {sd_prompt}")
                    sd_image_path = sd_api_t2i(sd_prompt, self.sd_path)
                    send_file(sd_image_path)
                    time.sleep(0.2)
                except Exception as e:
                    send_message("绘画失败")
                    self.logger.error(f"SD api error: {e}")
        if "//call video" in reply:
            reply = reply.replace("//call video", "")
            if self.call_times <= 0:
                call_video()
                if debug:
                    self.logger.debug(f"Call video.")
                    self.call_times += 1
                else:
                    self.call_times -= 0.1
                time.sleep(0.2)
        if "//touch_head" in reply:
            if self.debug:
                reply = reply.replace("//touch_head", "")
                head_shot()
                time.sleep(0.2)
        if self.tts:
            try:
                if self.debug:
                    self.logger.debug(f"TTS start.")
                send_message("TTS...")
                tts_dir = tts_service(self.tts_path, reply, self.cache_path)
                if self.debug:
                    self.logger.debug(f"TTS complete.File:{tts_dir}")
                if tts_dir:
                    send_file(tts_dir)
            except Exception as e:
                if self.debug:
                    self.logger.error(f"TTS error: {e}")
                send_message("哥哥！是不是你把我的声带偷了！！！：" + str(e))
        send_message(reply)

    def start(self):
        activate_wechat_window()
        self.check_cache()
        place = click_user()
        self.logger.debug(f"Main started")
        self.logger.info(f"LLM模型:{self.model}\n运行器:{self.launcher}")
        if place:
            if self.debug:
                send_message(f"[DEBUG]{self.model}已接入")
            click_user_next()
            if self.launcher == "fastchat":
                self.ai_agent = fcAIAgent(user_name=self.user)
            elif self.launcher == "ollama":
                self.ai_agent = olAIAgent(user_name=self.user, model=self.model, host=self.llm_path)
            elif self.launcher == "openai":
                self.ai_agent = oaAIAgent(user_name=self.user, model=self.model, host=self.llm_path, api_key=get_config("api_key"))
            else:
                raise ValueError("Invalid launcher")
            listener_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=self.on_press).start())
            listener_thread.start()
            last_chat_time = time.time()
            chat_delay = random.randint(300, 3600)
            self.logger.info(f"Auto chat delay:{chat_delay}")
            while not self.stop_flag or self.wechat_exit():
                place = check_unread_message()
                if place:
                    pag.click(x=place[0] + 30, y=place[1] + 20)
                    new_message = get_new_message()
                    if not new_message[1]:
                        continue
                    message_type = new_message[0]
                    if self.debug:
                        self.logger.info(f"New message:{new_message}")
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
                                    send_file(sd_api_t2i(new_message.split(" ")[1], self.sd_path))
                                    if self.debug:
                                        self.logger.debug(f"Sd draw.prompt{new_message.split(' ')[1]}")
                                elif new_message.split(" ")[0] == "#fadian":
                                    for i in range(random.randint(1, 1000)):
                                        send_message(f"{random.randint(1, 10000)}")
                                click_user_next()
                                continue
                            elif new_message.startswith("/"):
                                if new_message.split(" ")[0] == "/exit":
                                    self.logger.warning("Main exit.By wechat ")
                                    exit()
                                elif new_message.split(" ")[0] == "/help":
                                    send_message(self.get_help_wechat())
                                    self.logger.debug("Print help_text")
                                elif new_message.split(" ")[0] == "/tts":
                                    if self.tts:
                                        self.tts = False
                                    else:
                                        self.tts = True
                                    if self.debug:
                                        send_message(f"TTS:{self.tts}")
                                        self.logger.info(f"TTS change to {self.tts}")
                                    save_config("tts", self.tts)
                                elif new_message.split(" ")[0] == "/tts_status":
                                    send_message(f"TTS:{self.tts}")
                                    if self.debug:
                                        self.logger.info(f"Ask for TTS:{self.tts}")
                                elif new_message.split(" ")[0] == "/debug":
                                    if self.debug:
                                        self.debug = False
                                    else:
                                        self.debug = True
                                    if self.debug:
                                        send_message(f"debug:{self.debug}")
                                        self.logger.info(f"Debug change to {self.debug}")
                                    save_config("debug", self.debug)
                                elif new_message.split(" ")[0] == "/shutdown":
                                    send_message("哥哥你的电脑报废了...")
                                    self.logger.info("Shutdown.By wechat")
                                    os.system("shutdown -s -t 0")
                                elif new_message.split(" ")[0] == "/file":
                                    try:
                                        message_text = new_message.split(" ")[1]
                                    except IndexError:
                                        message_text = ""
                                    if self.debug:
                                        send_message("正在发送文件...")
                                        self.logger.info(f"Send file from {message_text}")
                                    send_file(message_text)
                                elif new_message.startswith("/dir"):
                                    try:
                                        message_text = new_message.split(" ")[1]
                                    except IndexError:
                                        message_text = ""
                                    if self.debug:
                                        send_message("正在发送文件夹目录...")
                                        self.logger.info(f"Send dir index from {message_text}")
                                    send_dir(message_text)
                                elif new_message == "/reset":
                                    os.remove(f"memories\\{self.user}.txt")
                                    if self.debug:
                                        send_message("记忆已重置")
                                        self.logger.info(f"Memory clear({self.user}).By wechat")
                                elif new_message.split(" ")[0] == "/model":
                                    if self.launcher == "ollama":
                                        model_list = olML(self.llm_path)
                                    else:
                                        model_list = fcML()
                                    if new_message.split(" ")[1] == "list":
                                        self.logger.debug(f"Get model list({model_list}).By wechat")
                                        send_message(str(model_list))
                                    elif new_message.split(" ")[1] == "set":
                                        new_model = new_message.split(" ")[2]
                                        if new_model in model_list:
                                            model = new_model
                                            send_message(f"已切换LLM模型为{model}")
                                            save_config("model", model)
                                            self.logger.debug(f"Model change to {model}.By wechat")
                                        else:
                                            send_message(f"无名为{new_model}的LLM模型")
                                            self.logger.warning(f"Model not found.{new_model}.By wechat")
                                    else:
                                        send_message(f"无名为{new_message}的指令")
                                        self.logger.warning(f"Command not found.{new_message}.By wechat")
                                click_user_next()
                                continue
                            send_message("少女思考中...")
                            self.logger.debug(f"Get response from {self.model}")
                            result = {}
                            try:
                                result['response'] = self.ai_agent.get_response((message_type, new_message))
                            except Exception as e:
                                result['response'] = "呜呜~思考过程中断了啦！"
                                self.logger.error(f"AI response error: {e}")

                            reply = result.get('response', "呜呜~我没有想好要说什么...")
                            self.message_process(reply)
                            time.sleep(0.2)
                            self.call_times -= 0.1
                        click_user_next()
                        last_chat_time = time.time()
                        chat_delay = random.randint(300, 3600)
                elif time.time() - last_chat_time >= chat_delay:
                    self.logger.info(f"Auto send Message.(wait time:{chat_delay})")
                    click_user()
                    reply = self.ai_agent.get_response(("auto", chat_delay))
                    self.logger.info(f"Auto message:{reply}")
                    self.message_process(reply)
                    last_chat_time = time.time()
                    chat_delay = random.randint(300, 3600)
            if self.wechat_exit():
                self.logger.critical("Wechat Exit.Main Stopped")
                return "WechatExit"
            else:
                send_message("用户中止")
                self.logger.info("Main Stopped by user")
                return "UserExit"
        else:
            self.logger.error(f"User not found.{self.user}")
            return f"UserNotFound(User: {self.user})"

    def get_info(self):
        self.logger.debug("Get info")
        return {"user": self.user, "launcher": self.launcher, "model": self.model, "l2d_model": self.l2d_model,
                "debug": self.debug, "tts": self.tts, "cache_path": self.cache_path, "llm_path": self.llm_path,
                "sd_path": self.sd_path, "enable_draw": self.enable_draw, "running": not self.stop_flag}

    def get_title(self):
        self.logger.debug("Get title")
        if os.path.exists(os.path.join("resources", "icon.txt")):
            return open(os.path.join("resources", "icon.txt"), encoding="utf-8").read()
        else:
            return None

    def get_help(self):
        self.logger.debug(f"""Load help text from{os.path.join(os.getcwd(), "resources", "command_help.txt")}""")
        if os.path.exists(os.path.join("resources", "command_help.txt")):
            return open(os.path.join("resources", "command_help.txt"), encoding="utf-8").read()
        else:
            return None

    def get_help_wechat(self):
        self.logger.debug(f"""Load wechat help text from{os.path.join(os.getcwd(), "resources", "command_help_wechat.txt")}""")
        if os.path.exists(os.path.join("resources", "command_help_wechat.txt")):
            return open(os.path.join("resources", "command_help_wechat.txt"), encoding="utf-8").read()
        else:
            return None

    def core_run(self):
        if self.user == "":
            self.logger.error(f"Core run error: User not set")
            raise ValueError("User has not init")
        else:
            self.logger.info(f"Core run: {self.user}")
            set_name(self.user)
            save_config("user", self.user)
            self.stop_flag = False
            time.sleep(2)
            self.start()

    def user_set(self, user_: str):
        if set_name(user_):
            self.user = user_
            save_config("user", self.user)
            self.logger.debug(f"User set: {self.user}")
            return True
        self.logger.error(f"User set error: User not found.{user_}")
        return False

    def user_add(self, user_info: dict):
        try:
            new_user = NewUser(user_info)
            new_user.generate_chosen()
            new_user.generate_mark()
            new_user.generate_touch()
            new_user.generate_image()
            new_user.add_set()
            self.user_set(user_info.get("name"))
            self.logger.debug(f"User add: {user_info.get('name')}")
            return True
        except Exception as e:
            self.logger.error(f"User add error: {e}")
            return e

    def user_memory_show(self):
        if os.path.exists(os.path.join("memories", f"{self.user}.txt")):
            memory = open(os.path.join("memories", f"{self.user}.txt")).readline()
            self.logger.debug(f"Get memory(User: {self.user}): {memory}")
            return memory
        else:
            self.logger.error(f"Memory not found.User: {self.user}")
            return None

    def user_memory_clear(self):
        if os.path.exists(os.path.join("memories", f"{self.user}.txt")):
            os.remove(os.path.join("memories", f"{self.user}.txt"))
            self.logger.debug(f"Memory clear: {self.user}")
            return True
        else:
            self.logger.error(f"Memory clear error(not found).User: {self.user}")
            return False

    def user_delete(self):
        file_list = [os.path.join("set", f"{self.user}.txt"), os.path.join("memories", f"{self.user}.txt"),
                     os.path.join("resources", "images", self.user, f"chosen.png"),
                     os.path.join("resources", "images", self.user, f"image.png"),
                     os.path.join("resources", "images", self.user, f"mark.png"),
                     os.path.join("resources", "images", self.user, f"touch_head.txt")]
        for file in file_list:
            if os.path.exists(file):
                os.remove(file)
        self.logger.debug(f"User delete: {self.user}")
        return True

    def user_list(self):
        user_list = os.listdir("set")
        for index in range(len(user_list)):
            if user_list[index].endswith(".txt"):
                user_list[index] = user_list[index][:-4]
        self.logger.debug(f"Get user list {user_list}")
        return user_list

    def llm_model_set(self, model_: str):
        model_list = self.llm_model_list()
        if model_list:
            if model_ in model_list:
                self.model = model_
                save_config("model", self.model)
                return True
            else:
                raise FileNotFoundError(f"Model {model_} not found")
        else:
            self.model = model_
            save_config("model", self.model)
            return True

    def llm_model_list(self):
        if self.launcher == "ollama":
            model_list = olML(self.llm_path)
        elif self.launcher == "fastchat":
            model_list = fcML()
        elif self.launcher == "openai":
            model_list = oaML(self.llm_path)
        else:
            raise ValueError("Launcher not found")
        self.logger.debug(f"Get {self.launcher} LLM model list: {model_list}")
        return model_list

    def llm_model_launcher_set(self, runner_: str):
        self.logger.debug(f"Set {runner_} as LLM launcher")
        self.launcher = runner_
        save_config("launcher", self.launcher)
        return True

    def tts_set(self):
        try:
            self.tts = not self.tts
            self.logger.debug(f"Set TTS: {self.tts}")
            save_config("tts", self.tts)
            return True
        except Exception as e:
            self.logger.error(f"TTS set error: {e}")
            return e

    def l2d_model_set(self, model_: str):
        model_list = self.l2d_model_list()
        if model_ in model_list:
            self.l2d_model = model_
            save_config("l2d_model", self.l2d_model)
            self.logger.debug(f"Set L2D model: {model_}")
            return True
        else:
            raise FileNotFoundError(f"L2D model {model_} not found")

    def l2d_model_list(self):
        model_list = os.listdir(os.path.join("l2d_models"))
        self.logger.debug(f"Get L2D model list: {model_list}")
        return model_list

    def l2d_model_add(self, input_model):
        if os.path.exists(input_model) and os.path.isdir(input_model):
            shutil.copytree(input_model, f"l2d_model\\{os.path.basename(input_model)}")
            save_config("l2d_model", os.path.basename(input_model))
            self.logger.debug(f"Live2D model added {os.path.basename(input_model)}")
            return True
        return False

    def l2d_model_delete(self, model_: str):
        if os.path.exists(os.path.join("l2d_models", model_)):
            shutil.rmtree(os.path.join("l2d_models", model_))
            save_config("l2d_model", "")
            self.logger.debug(f"Live2D model delete: {model_}")
            return True
        else:
            self.logger.error(f"Live2D model delete error: {model_} not found")
            return False

    def set_debug(self):
        try:
            self.debug = not self.debug
            self.logger.debug(f"Set debug: {self.debug}")
            save_config("debug", self.debug)
            return True
        except Exception as e:
            self.logger.error(f"Set debug error: {e}")
            return e

    def set_draw(self):
        try:
            self.enable_draw = not self.enable_draw
            self.logger.debug(f"Set draw: {self.enable_draw}")
            save_config("enable_draw", self.enable_draw)
            return True
        except Exception as e:
            self.logger.error(f"Set draw error: {e}")
            return e

    def set_cache_clear(self):
        self.logger.debug(f"Clear cache")
        if os.path.exists(self.cache_path):
            shutil.rmtree(self.cache_path)
            os.makedirs(self.cache_path, exist_ok=True)
        self.logger.debug("Cache clear")
        return True

    def set_cache_set(self, cache_path_: str):
        self.logger.debug(f"Set cache path: {cache_path_}")
        self.cache_path = cache_path_
        os.makedirs(self.cache_path, exist_ok=True)
        save_config("cache_path", self.cache_path)
        return True

    def set_llm_path(self, llm_path_: str):
        self.logger.debug(f"Set LLM path: {llm_path_}")
        self.llm_path = llm_path_
        save_config("llm_path", self.llm_path)
        return True

    def set_sd_path(self, sd_path_: str):
        self.logger.debug(f"Set SD path: {sd_path_}")
        self.sd_path = sd_path_
        save_config("sd_path", self.sd_path)
        return True

    def set_tts_path(self, tts_path_: str):
        self.logger.debug(f"Set TTS path: {tts_path_}")
        self.tts_path = tts_path_
        save_config("tts_path", self.tts_path)
        return True
