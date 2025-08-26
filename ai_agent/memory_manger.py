# memory_manager.py
import logging
import os


class MemoryManager:
    def __init__(self, user_name="zheng"):
        self.logger = logging.getLogger("memory manger")
        self.logger_formatter = logging.Formatter("[%(levelname)s][%(name)s]%(message)s")
        self.user_name = user_name
        self.memory_dir = os.path.join(os.getcwd(), "memories")
        self.memory_path = os.path.join(self.memory_dir, f"{self.user_name}.txt")
        self._ensure_memory_file()

    def _ensure_memory_file(self):
        if not os.path.exists(self.memory_dir):
            os.makedirs(self.memory_dir)
        if not os.path.exists(self.memory_path):
            with open(self.memory_path, "w+", encoding="utf-8") as f:
                f.write("")

    def load_memory(self):
        self.logger.debug(f"Load memory from {self.memory_path}")
        try:
            with open(self.memory_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            self.logger.error(f"Load memory failed: {e}")
            return ""

    def save_memory(self, content):
        self.logger.debug(f"Save memory to {self.memory_path}")
        try:
            with open(self.memory_path, "a", encoding="utf-8") as f:
                f.write(content + "\n")
        except Exception as e:
            self.logger.error(f"Save memory failed: {e}")
