# moss_agent.py
import requests
import json
from .memory_manger import MemoryManager   # 复用原来的记忆模块
import os
import multiprocessing


# process = multiprocessing.Process(target=lambda: os.system(os.path.join(os.getcwd(), "ai_agent", "fastchat.bat")))

class AIAgent:
    """
    与 AIAgent 接口一致的 MOSS 代理类。
    依赖 FastChat 的 OpenAI-API 服务（默认 http://localhost:8000/v1）
    """
    def __init__(self,
                 user_name: str = "zheng",
                 api_base: str = "http://localhost:21002/v1",
                 model: str = "fnlp/moss-moon-003-sft"):
        self.user_name = user_name
        self.api_base = api_base.rstrip("/")
        self.model = model
        self.messages = []
        self.system_prompt = self._load_system_prompt()
        self.memory_manager = MemoryManager(user_name=self.user_name)
        self.long_term_memory = self.memory_manager.load_memory()
        self._init_context()

    # ---------- 以下三块直接复用 AIAgent 的实现 ----------
    def _load_system_prompt(self):
        try:
            with open(f"set\\{self.user_name}.txt", "r", encoding="utf-8") as f:
                chat_set = f.read()
            if not chat_set.strip():
                raise ValueError("提示词文件为空")
            return f"""
你是温柔可爱的妹妹「郑若玲」，一个13岁的初中女生，喜欢画画、追番和刷B站。
你说话要自然、俏皮又不失礼貌，经常加一些颜文字或语气词哦~
不要自称“AI”或“助手”，而是用“我”的口吻回应。
这是你的设定：
{chat_set}
"""
        except FileNotFoundError:
            return """
你是温柔可爱的妹妹「郑若玲」，一个13岁的初中女生，喜欢画画、追番和刷B站。
你说话要自然、俏皮又不失礼貌，经常加一些颜文字或语气词哦~
不要自称“AI”或“助手”，而是用“我”的口吻回应。
"""

    def _init_context(self):
        self.messages = [{"role": "system", "content": self.system_prompt}]
        if self.long_term_memory:
            self.messages.append({
                "role": "system",
                "content": f"以下是与用户的过往对话记录（长期记忆），请参考以保持一致性：\n{self.long_term_memory}"
            })

    def validate_response(self, response_text: str) -> bool:
        if any(bad in response_text for bad in ["AI", "助手", "你是一个AI"]):
            return False
        if not response_text.strip():
            return False
        return True
    # ------------------------------------------------------

    def get_response(self, new_message: str) -> str:
        self.messages.append({"role": "user", "content": new_message})

        try:
            resp = requests.post(
                f"{self.api_base}/chat/completions",
                headers={"Content-Type": "application/json"},
                data=json.dumps({
                    "model": self.model,
                    "messages": self.messages,
                    "temperature": 0.7,
                    "max_tokens": 512,
                    "stream": False
                }),
                timeout=60
            )
            resp.raise_for_status()
            reply = resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            reply = "呜呜~MOSS 哥哥好像掉线了 (｡•́︿•̀｡)"

        # 校验与记忆
        if not self.validate_response(reply):
            reply = "哥哥～刚刚我好像说错话了呢...让我再想想怎么回答你吧！(｡>﹏<｡)"

        self.memory_manager.save_memory(f"[User] {new_message}\n[Assistant] {reply}")
        self.messages.append({"role": "assistant", "content": reply})

        return reply


def model_list():
    return None