import logging

from ollama import chat, ChatResponse, list, Client
from .memory_manger import MemoryManager
from .bing_crawler import search_bing


class AIAgent:
    def __init__(self, host="http://localhost:11434", user_name="zheng", model="qwen3:0.6b"):
        self.logger = logging.getLogger("LLM_ollama")
        self.logger_formatter = logging.Formatter("[%(levelname)s][%(name)s]%(message)s")
        self.user_name = user_name
        self.model = model
        self.message = []
        self.system_prompt = self._load_system_prompt()
        self._load_system_format()
        self.memory_manager = MemoryManager(user_name=self.user_name)
        self.long_term_memory = self.memory_manager.load_memory()
        self._init_context()
        self.recent_replies = []  # 新增一个列表记录最近回复
        self.max_history = 5  # 设置最大历史记录数
        self.client = Client(host=host, headers={'x-some-header': 'some-value'})

    def _load_system_prompt(self):
        try:
            with open(f"set\\{self.user_name}.txt", "r", encoding="utf-8") as f:
                chat_set = f.read()
            if not chat_set.strip():
                self.logger.warning("Prompt load failed.Use Default")
                raise ValueError("提示词文件为空")
            self.logger.debug(f"Prompt load complete:{chat_set}")
            return chat_set
        except FileNotFoundError:
            self.logger.warning("Prompt load failed.Use Default")
            return """
你是温柔可爱的妹妹「郑若玲」，一个13岁的初中女生，喜欢画画、追番和刷B站。
你说话要自然、俏皮又不失礼貌，经常加一些颜文字或语气词哦~
不要自称“AI”或“助手”，而是用“我”的口吻回应。
"""
        except Exception as e:
            self.logger.error(f"Prompt load failed.{e}")
            return ""

    def _load_system_format(self):
        try:
            with open(f"./ai_agent/system_format.txt", "r", encoding="utf-8") as f:
                self.system_format = f.read()
            if not self.system_format.strip():
                self.system_format = ""
                self.logger.warning("System format load failed.Use Default")
                raise ValueError("格式文件为空")
            self.logger.debug(f"System format load complete:{self.system_format}")
            return self.system_format
        except FileNotFoundError:
            self.system_format = ""
            self.logger.warning("System format load failed.File Not Found")
            raise FileNotFoundError("格式文件不存在")

    def _init_context(self):
        init_messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        if self.long_term_memory:
            init_messages.append({
                "role": "system",
                "content": f"以下是与用户的过往对话记录（长期记忆），请参考以保持一致性：\n{self.long_term_memory}"
            })
        self.message = init_messages

    def validate_response(self, response_text):
        """校验回复是否符合角色设定"""
        filter_list = ["AI", "助手", "你是一个AI"]
        if any(bad in response_text for bad in filter_list):
            self.logger.warning(f"Response included {filter_list}")
            return False
        if not response_text.strip():
            self.logger.warning("Response is empty")
            return False
        return True

    def get_response(self, new_message, memory=True):
        try:
            if memory:
                if new_message[0] == "text":
                    new_message = new_message[1]
                    self.message.append({"role": "user", "content": new_message})
                    self.memory_manager.save_memory(f"[user] {new_message}")
                    bing_response = search_bing(new_message)
                    self.logger.info(f"Bing response:{bing_response}")
                    response: ChatResponse = self.client.chat(model=self.model, messages=[
                        {"role": "system", "content": f"以下是你的记忆：{self.message}"},
                        {"role": "system", "content": f"以下是你和用户的设定：{self.system_prompt}"},
                        {"role": "system",
                         "content": f"必须严格遵循以下格式，不得增删任何说明文字：\n{self.system_format}"},
                        {"role": "system", "content": f"基于设定，回答user的问题"},
                        {"role": "web", "content": f"{bing_response}"},
                        {"role": "user", "content": new_message}
                    ], think=False)
                elif new_message[0] == "image":
                    new_message = new_message[1]
                    response: ChatResponse = self.client.chat(model=self.model, messages=[
                        {"role": "system", "content": f"以下是你的记忆：{self.message}"},
                        {"role": "system", "content": f"以下是你和用户的设定：{self.system_prompt}"},
                        {"role": "system",
                         "content": f"必须严格遵循以下格式，不得增删任何说明文字：\n{self.system_format}"},
                        {"role": "system", "content": f"基于设定，回答user的问题"},
                        {"role": "system", "content": f"用户发送了如下的图片", "image": new_message}
                    ], think=False)
                elif new_message[0] == "auto":
                    response: ChatResponse = self.client.chat(model=self.model, messages=[
                        {"role": "system", "content": f"以下是你的记忆：{self.message}"},
                        {"role": "system", "content": f"以下是你和用户的设定：{self.system_prompt}"},
                        {"role": "system",
                         "content": f"必须严格遵循以下格式，不得增删任何说明文字：\n{self.system_format}"},
                        {"role": "system", "content": f"用户已经{new_message[1]}秒没给你发消息了，基于设定，请主动发一段消息。"},
                    ], think=False)
                else:
                    raise ValueError("无效的消息类型")
            else:
                response: ChatResponse = self.client.chat(model=self.model, messages=[{"role": "user", "content":new_message}   ], think=True)
            reply = response['message']['content']
            self.logger.info(f"Ollama reply:{reply}")
            if memory:
                self.message.append({"role": "assistant", "content": reply})
        except Exception as e:
            reply = "呜呜~模型出错了啦！"
            self.logger.error(f"Ollama error:{e}")

        # 如果回复中包含 <think> 标签，则只校验 </think> 后的内容
        if memory:
            # 校验回复内容
            if not self.validate_response(reply):
                reply = "哥哥～刚刚我好像说错话了呢...让我再想想怎么回答你吧！(｡>﹏<｡)"

        if memory:
            self.memory_manager.save_memory(f"[Assistant] {reply}")
        return reply


def model_list(host="https://localhost:11434"):
    """
    获取模型列表
    """
    client = Client(host=host, headers={'x-some-header': 'some-value'})
    models = []
    for model in client.list()["models"]:
        models.append(model["model"])
    return models
