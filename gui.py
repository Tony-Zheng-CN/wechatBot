import tkinter
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
import sys
import logging
import os
import shutil
from PIL import Image, ImageTk

try:
    # noinspection PyUnresolvedReferences
    import ttkbootstrap

    tk = ttkbootstrap
except ImportError:
    tk = tkinter
from core import *


# 创建一个自定义的日志处理器，将日志输出到GUI文本框
class GuiLogHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.see(tk.END)
        self.text_widget.update()


# 创建一个自定义的stdout重定向类
class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)
        self.text_widget.update()

    def flush(self):
        pass


# 添加用户对话框
class AddUserDialog(tk.Toplevel):
    def __init__(self, parent, core):
        super().__init__(parent)
        self.title("添加用户")
        self.geometry("400x500")
        self.core = core

        # 用户信息变量
        self.username = tk.StringVar()
        self.user_image_path = tk.StringVar()
        self.user_name = tk.StringVar()
        self.user_age = tk.StringVar()
        self.user_gender = tk.StringVar()
        self.user_personality = tk.StringVar()
        self.user_hobbies = tk.StringVar()
        self.user_background = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # 用户名
        tk.Label(self, text="用户名:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(self, textvariable=self.username, width=30).grid(row=0, column=1, padx=5, pady=5)

        # 用户头像
        tk.Label(self, text="用户头像:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(self, textvariable=self.user_image_path, width=25).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self, text="浏览", command=self.browse_image).grid(row=1, column=2, padx=5, pady=5)

        # 用户姓名
        tk.Label(self, text="姓名:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(self, textvariable=self.user_name, width=30).grid(row=2, column=1, padx=5, pady=5)

        # 用户年龄
        tk.Label(self, text="年龄:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(self, textvariable=self.user_age, width=30).grid(row=3, column=1, padx=5, pady=5)

        # 用户性别
        tk.Label(self, text="性别:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(self, textvariable=self.user_gender, width=30).grid(row=4, column=1, padx=5, pady=5)

        # 用户性格
        tk.Label(self, text="性格:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(self, textvariable=self.user_personality, width=30).grid(row=5, column=1, padx=5, pady=5)

        # 用户爱好
        tk.Label(self, text="爱好:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(self, textvariable=self.user_hobbies, width=30).grid(row=6, column=1, padx=5, pady=5)

        # 用户背景
        tk.Label(self, text="背景:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(self, textvariable=self.user_background, width=30).grid(row=7, column=1, padx=5, pady=5)

        # 按钮
        button_frame = tk.Frame(self)
        button_frame.grid(row=8, column=0, columnspan=3, pady=20)

        tk.Button(button_frame, text="添加", command=self.add_user).pack(side="left", padx=5)
        tk.Button(button_frame, text="取消", command=self.destroy).pack(side="left", padx=5)

    def browse_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.user_image_path.set(file_path)

    def add_user(self):
        # 检查必填字段
        if not self.username.get():
            messagebox.showerror("错误", "请输入用户名")
            return

        try:
            # 创建用户信息字典
            user_info = {
                "username": self.username.get(),
                "name": self.user_name.get() or "未设置",
                "age": self.user_age.get() or "未设置",
                "sex": self.user_gender.get() or "未设置",
                "hobby": self.user_hobbies.get() or "未设置",
                "personality": self.user_personality.get() or "未设置",
                "background": self.user_background.get() or "未设置"
            }

            # 调用core中的用户添加方法
            result = self.core.user_add(user_info)

            if result is True:
                # 复制用户头像（如果提供了）
                if self.user_image_path.get():
                    self.copy_user_image()

                messagebox.showinfo("成功", f"用户 {self.username.get()} 添加成功")
                self.destroy()
            else:
                messagebox.showerror("错误", f"添加用户失败: {result}")
        except Exception as e:
            messagebox.showerror("错误", f"添加用户时发生错误: {str(e)}")

    def copy_user_image(self):
        try:
            # 创建用户资源目录
            user_resource_dir = os.path.join("resources", "images", self.username.get())
            os.makedirs(user_resource_dir, exist_ok=True)

            # 复制用户头像
            if os.path.exists(self.user_image_path.get()):
                # 原始图像路径
                src_image_path = self.user_image_path.get()

                # 目标图像路径
                dst_image_path = os.path.join(user_resource_dir, "image.png")

                # 复制并调整图像大小
                image = Image.open(src_image_path)
                image = image.resize((50, 50), Image.Resampling.LANCZOS)
                image.save(dst_image_path)

                # 生成其他所需图像
                self.generate_mark_image(user_resource_dir, dst_image_path)
                self.generate_chosen_image(user_resource_dir, dst_image_path)
                self.generate_touch_image(user_resource_dir, dst_image_path)
        except Exception as e:
            print(f"复制用户图像时出错: {e}")

    def generate_mark_image(self, user_dir, image_path):
        try:
            # 创建背景图像 (32x32)
            background = Image.new("RGB", (32, 32), "#EBE9E8")

            # 打开并裁剪用户头像的右上角部分
            avatar = Image.open(image_path)
            cropped_avatar = avatar.crop((50 - 27, 0, 50, 22))

            # 将裁剪后的头像粘贴到背景的右下角
            background.paste(cropped_avatar, (0, 10))

            # 加载并粘贴 unread_mark.png 到顶部居中
            unread_mark_path = os.path.join("resources", "images", "unread_mark.png")
            if os.path.exists(unread_mark_path):
                unread_mark = Image.open(unread_mark_path).convert("RGBA")
                unread_mark = unread_mark.resize((16, 16), Image.Resampling.LANCZOS)
                background.paste(unread_mark, (16, 0), unread_mark)

            mark_path = os.path.join(user_dir, "mark.png")
            background.save(mark_path)
        except Exception as e:
            print(f"生成mark图像时出错: {e}")

    def generate_chosen_image(self, user_dir, image_path):
        try:
            # 创建背景图像 (60x60)
            background = Image.new("RGB", (60, 60), "#C8C8CA")

            # 打开用户头像
            avatar = Image.open(image_path)

            # 将头像粘贴到背景中心
            background.paste(avatar, (5, 5))

            chosen_path = os.path.join(user_dir, "chosen.png")
            background.save(chosen_path)
        except Exception as e:
            print(f"生成chosen图像时出错: {e}")

    def generate_touch_image(self, user_dir, image_path):
        try:
            # 打开背景图像
            touch_background_path = os.path.join("resources", "images", "touch_head.png")
            if os.path.exists(touch_background_path):
                background = Image.open(touch_background_path)

                # 打开用户头像并缩放
                avatar = Image.open(image_path)
                resized_avatar = avatar.resize((42, 40), Image.Resampling.LANCZOS)

                # 粘贴到右侧最上方
                background.paste(resized_avatar, (background.width - resized_avatar.width, 0))

                touch_path = os.path.join(user_dir, "touch_head.png")
                background.save(touch_path)
        except Exception as e:
            print(f"生成touch图像时出错: {e}")


class App:
    def __init__(self):
        self.logger = logging.getLogger("GUI")
        self.core = WeChatBot()
        if tk == tkinter:
            self.win = tkinter.Tk()
        elif tk == ttkbootstrap:
            self.win = ttkbootstrap.Window()
        self.win.title(f"WeChatBotGUI")
        self.win.geometry("800x600")
        self._create_widgets()

        # 重定向stdout和stderr到GUI文本框
        sys.stdout = StdoutRedirector(self.output_text)
        sys.stderr = StdoutRedirector(self.output_text)

        # 添加日志处理器，将日志输出到GUI文本框
        gui_handler = GuiLogHandler(self.output_text)
        gui_handler.setFormatter(logging.Formatter('[%(levelname)s][%(name)s]%(message)s'))
        logging.getLogger().addHandler(gui_handler)

        # 设置日志级别
        logging.getLogger().setLevel(logging.DEBUG)

    def _update_vars(self):
        core_info = self.core.get_info()
        self.debug.set(core_info.get("debug"))
        self.tts.set(core_info.get("tts"))
        self.draw.set(core_info.get("enable_draw"))
        self.running.set(core_info.get("running"))
        self.tts_path.set(core_info.get("tts_path"))
        self.llm_path.set(core_info.get("llm_path"))
        self.sd_path.set(core_info.get("sd_path"))
        self.user.set(core_info.get("user"))
        self.model.set(core_info.get("model"))
        self.launcher.set(core_info.get("launcher"))
        self.cache_path.set(core_info.get("cache_path"))
        self.l2d_model.set(core_info.get("l2d_model"))

    def update_tk(self):
        self._update_vars()
        user_list = self.core.user_list()
        model_list = self.core.llm_model_list()

        self.user_ccb.config(values=user_list)
        self.model_ccb.config(values=model_list)
        self.launcher_ccb.config(values=["ollama", "fastchat", "openai"])

    def _create_widgets(self):
        self.logger.info("Creating widgets...")

        # 创建变量
        self.running = tk.BooleanVar()
        self.debug = tk.BooleanVar()
        self.tts = tk.BooleanVar()
        self.draw = tk.BooleanVar()
        self.user = tk.StringVar()
        self.model = tk.StringVar()
        self.launcher = tk.StringVar()
        self.cache_path = tk.StringVar()
        self.tts_path = tk.StringVar()
        self.llm_path = tk.StringVar()
        self.sd_path = tk.StringVar()
        self.l2d_model = tk.StringVar()
        self._update_vars()

        # 获取窗口尺寸
        self.win.update()
        height = self.win.winfo_height() or 600
        width = self.win.winfo_width() or 800

        # 创建容器
        self.output_frame = tk.Frame(self.win, width=width // 2, height=height)
        self.info_frame = tk.Frame(self.win, width=width // 2, height=height // 4 * 3)
        self.control_frame = tk.Frame(self.win, width=width // 2, height=height // 4)

        # 创建控件(output_frame)
        self.output_text = tk.Text(self.output_frame, width=width // 3 * 2 // 8, height=height // 20)
        self.output_scrollbar = tk.Scrollbar(self.output_frame, orient="vertical", command=self.output_text.yview)
        self.output_text.config(yscrollcommand=self.output_scrollbar.set)

        # 创建控件(info_frame)
        self.debug_rb = tk.Checkbutton(self.info_frame, text="Debug: ", variable=self.debug, command=self.toggle_debug)
        self.tts_rb = tk.Checkbutton(self.info_frame, text="TTS: ", variable=self.tts, command=self.toggle_tts)
        self.draw_rb = tk.Checkbutton(self.info_frame, text="Enable draw: ", variable=self.draw,
                                      command=self.toggle_draw)

        self.user_label = tk.Label(self.info_frame, text="User: ")
        self.user_ccb = ttk.Combobox(self.info_frame, textvariable=self.user, state="readonly")

        self.model_label = tk.Label(self.info_frame, text="Model: ")
        # 修复语法错误：使用正确的三元运算符
        model_list = self.core.llm_model_list()
        state = "readonly" if model_list else "normal"
        self.model_ccb = ttk.Combobox(self.info_frame, textvariable=self.model, state=state)

        self.launcher_label = tk.Label(self.info_frame, text="Launcher: ")
        self.launcher_ccb = ttk.Combobox(self.info_frame, textvariable=self.launcher, state="readonly")

        # 使用StringVar的值而不是直接获取
        self.cache_path_label = tk.Label(self.info_frame, textvariable=self.cache_path)
        self.tts_path_label = tk.Label(self.info_frame, textvariable=self.tts_path)
        self.llm_path_label = tk.Label(self.info_frame, textvariable=self.llm_path)
        self.sd_path_label = tk.Label(self.info_frame, textvariable=self.sd_path)
        self.l2d_model_label = tk.Label(self.info_frame, textvariable=self.l2d_model)

        # 创建控件(control_frame)
        self.start_button = tk.Button(self.control_frame, text="Start", command=self.start_core)
        self.settings_button = tk.Button(self.control_frame, text="Settings", command=self.open_settings)
        self.user_button = tk.Button(self.control_frame, text="User Management", command=self.open_user_management)

        # 布局
        self.output_text.pack(side="left", fill="both", expand=True)
        self.output_scrollbar.pack(side="right", fill="y")

        self.debug_rb.grid(row=0, column=0, sticky="w")
        self.tts_rb.grid(row=0, column=1, sticky="w")
        self.draw_rb.grid(row=0, column=2, sticky="w")

        self.user_label.grid(row=1, column=0, sticky="w")
        self.user_ccb.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5)

        self.model_label.grid(row=2, column=0, sticky="w")
        self.model_ccb.grid(row=2, column=1, columnspan=3, sticky="ew", padx=5)

        self.launcher_label.grid(row=3, column=0, sticky="w")
        self.launcher_ccb.grid(row=3, column=1, columnspan=3, sticky="ew", padx=5)

        # 更新标签文本
        self.update_labels()

        self.start_button.pack(pady=5, fill="x")
        self.settings_button.pack(pady=5, fill="x")
        self.user_button.pack(pady=5, fill="x")

        # 配置网格权重
        self.info_frame.grid_columnconfigure(1, weight=1)
        self.info_frame.grid_columnconfigure(2, weight=1)
        self.info_frame.grid_columnconfigure(3, weight=1)

        self.info_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.control_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.output_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)

        # 配置主窗口网格权重
        self.win.grid_columnconfigure(0, weight=1)
        self.win.grid_columnconfigure(1, weight=1)
        self.win.grid_rowconfigure(0, weight=1)
        self.win.grid_rowconfigure(1, weight=0)

        self.update_tk()

        # 绑定事件
        self.user_ccb.bind("<<ComboboxSelected>>", self.on_user_selected)
        self.model_ccb.bind("<<ComboboxSelected>>", self.on_model_selected)
        self.launcher_ccb.bind("<<ComboboxSelected>>", self.on_launcher_selected)

    def update_labels(self):
        # 更新显示配置信息的标签
        self.cache_path.set(f"Cache path: {self.core.cache_path}")
        self.tts_path.set(f"TTS path: {self.core.tts_path}")
        self.llm_path.set(f"LLM path: {self.core.llm_path}")
        self.sd_path.set(f"SD path: {self.core.sd_path}")
        self.l2d_model.set(f"Live2D model: {self.core.l2d_model}")

    def on_user_selected(self, event):
        selected_user = self.user.get()
        if selected_user:
            self.core.user_set(selected_user)

    def on_model_selected(self, event):
        selected_model = self.model.get()
        if selected_model:
            try:
                self.core.llm_model_set(selected_model)
                self.log_message(f"Model set to: {selected_model}")
            except Exception as e:
                self.log_message(f"Error setting model: {e}")

    def on_launcher_selected(self, event):
        selected_launcher = self.launcher.get()
        if selected_launcher in ["ollama", "fastchat", "openai"]:
            try:
                self.core.llm_model_launcher_set(selected_launcher)
                self.log_message(f"Launcher set to: {selected_launcher}")
                # 更新模型列表
                self.update_tk()
            except Exception as e:
                self.log_message(f"Error setting launcher: {e}")

    def toggle_debug(self):
        try:
            self.core.set_debug()
            self.log_message(f"Debug mode: {'enabled' if self.core.debug else 'disabled'}")
        except Exception as e:
            self.log_message(f"Error toggling debug: {e}")

    def toggle_tts(self):
        try:
            self.core.tts_set()
            self.log_message(f"TTS: {'enabled' if self.core.tts else 'disabled'}")
        except Exception as e:
            self.log_message(f"Error toggling TTS: {e}")

    def toggle_draw(self):
        try:
            # 注意：core.py中没有直接的set_draw方法，我们需要通过配置管理来实现
            self.core.enable_draw = self.draw.get()
            from config_manager import save_config
            save_config("draw", self.core.enable_draw)
            self.log_message(f"Draw feature: {'enabled' if self.core.enable_draw else 'disabled'}")
        except Exception as e:
            self.log_message(f"Error toggling draw: {e}")

    def start_core(self):
        try:
            self.logger.info("Starting core...")
            self.log_message("Starting core...")
            # 在新线程中运行core，避免阻塞GUI
            import threading
            thread = threading.Thread(target=self._run_core)
            thread.daemon = True
            thread.start()
        except Exception as e:
            self.logger.error(f"Failed to start core: {e}")
            self.log_message(f"Error: {e}")

    def _run_core(self):
        try:
            self.core.core_run()
        except Exception as e:
            self.log_message(f"Core error: {e}")

    def open_settings(self):
        settings_window = tk.Toplevel(self.win)
        settings_window.title("Settings")
        settings_window.geometry("500x400")

        # 创建notebook用于分页
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # 路径设置标签页
        path_frame = ttk.Frame(notebook)
        notebook.add(path_frame, text="Paths")

        # LLM路径
        tk.Label(path_frame, text="LLM Path:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        llm_path_entry = tk.Entry(path_frame, textvariable=tk.StringVar(value=self.core.llm_path), width=40)
        llm_path_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(path_frame, text="Browse", command=lambda: self.browse_path(llm_path_entry, "llm")).grid(row=0,
                                                                                                           column=2,
                                                                                                           padx=5,
                                                                                                           pady=5)

        # SD路径
        tk.Label(path_frame, text="SD Path:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        sd_path_entry = tk.Entry(path_frame, textvariable=tk.StringVar(value=self.core.sd_path), width=40)
        sd_path_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(path_frame, text="Browse", command=lambda: self.browse_path(sd_path_entry, "sd")).grid(row=1,
                                                                                                         column=2,
                                                                                                         padx=5, pady=5)

        # TTS路径
        tk.Label(path_frame, text="TTS Path:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tts_path_entry = tk.Entry(path_frame, textvariable=tk.StringVar(value=self.core.tts_path), width=40)
        tts_path_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(path_frame, text="Browse", command=lambda: self.browse_path(tts_path_entry, "tts")).grid(row=2,
                                                                                                           column=2,
                                                                                                           padx=5,
                                                                                                           pady=5)

        # 缓存路径
        tk.Label(path_frame, text="Cache Path:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        cache_path_entry = tk.Entry(path_frame, textvariable=tk.StringVar(value=self.core.cache_path), width=40)
        cache_path_entry.grid(row=3, column=1, padx=5, pady=5)
        tk.Button(path_frame, text="Browse", command=lambda: self.browse_path(cache_path_entry, "cache")).grid(row=3,
                                                                                                               column=2,
                                                                                                               padx=5,
                                                                                                               pady=5)

        # 模型设置标签页
        model_frame = ttk.Frame(notebook)
        notebook.add(model_frame, text="Models")

        # 当前模型
        tk.Label(model_frame, text="Current Model:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        model_entry = tk.Entry(model_frame, textvariable=tk.StringVar(value=self.core.model), width=40)
        model_entry.grid(row=0, column=1, padx=5, pady=5)

        # Live2D模型
        tk.Label(model_frame, text="Live2D Model:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        l2d_model_entry = tk.Entry(model_frame, textvariable=tk.StringVar(value=self.core.l2d_model), width=40)
        l2d_model_entry.grid(row=1, column=1, padx=5, pady=5)

        # API密钥标签页
        api_frame = ttk.Frame(notebook)
        notebook.add(api_frame, text="API Keys")

        # API密钥（如果需要）
        tk.Label(api_frame, text="API Key:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        api_key_entry = tk.Entry(api_frame, width=40, show="*")
        api_key_entry.grid(row=0, column=1, padx=5, pady=5)

        # 按钮框架
        button_frame = tk.Frame(settings_window)
        button_frame.pack(pady=10)

        # 保存按钮
        tk.Button(button_frame, text="Save", command=lambda: self.save_settings(
            llm_path_entry.get(), sd_path_entry.get(), tts_path_entry.get(),
            cache_path_entry.get(), model_entry.get(), l2d_model_entry.get()
        )).pack(side="left", padx=5)

        # 取消按钮
        tk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side="left", padx=5)

        # 重置按钮
        tk.Button(button_frame, text="Reset", command=lambda: self.reset_settings(
            llm_path_entry, sd_path_entry, tts_path_entry, cache_path_entry,
            model_entry, l2d_model_entry
        )).pack(side="left", padx=5)

    def open_user_management(self):
        user_window = tk.Toplevel(self.win)
        user_window.title("用户管理")
        user_window.geometry("400x300")

        # 用户列表
        tk.Label(user_window, text="用户列表:").pack(pady=5)

        # 创建列表框和滚动条
        list_frame = tk.Frame(user_window)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        user_listbox = tk.Listbox(list_frame)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=user_listbox.yview)
        user_listbox.config(yscrollcommand=scrollbar.set)

        # 填充用户列表
        users = self.core.user_list()
        for user in users:
            user_listbox.insert(tk.END, os.path.splitext(user)[0])

        user_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 按钮框架
        button_frame = tk.Frame(user_window)
        button_frame.pack(pady=10)

        # 添加用户按钮
        tk.Button(button_frame, text="添加用户", command=self.add_user).pack(side="left", padx=5)

        # 删除用户按钮
        tk.Button(button_frame, text="删除用户", command=lambda: self.delete_user(user_listbox)).pack(side="left",
                                                                                                      padx=5)

        # 设置当前用户按钮
        tk.Button(button_frame, text="设为当前用户", command=lambda: self.set_current_user(user_listbox)).pack(
            side="left", padx=5)

    def add_user(self):
        # 打开添加用户对话框
        dialog = AddUserDialog(self.win, self.core)
        self.win.wait_window(dialog)
        # 更新用户列表
        self.update_tk()

    def delete_user(self, listbox):
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个用户")
            return

        user_name = listbox.get(selection[0])
        if messagebox.askyesno("确认", f"确定要删除用户 {user_name} 吗？"):
            try:
                # 调用core中的用户删除方法
                self.core.user_delete()
                # 删除用户相关文件
                self.remove_user_files(user_name)
                # 更新用户列表
                self.update_tk()
                # 从列表框中移除
                listbox.delete(selection[0])
                messagebox.showinfo("成功", f"用户 {user_name} 已删除")
            except Exception as e:
                messagebox.showerror("错误", f"删除用户失败: {str(e)}")

    def remove_user_files(self, user_name):
        try:
            # 删除用户设置文件
            set_file = os.path.join("set", f"{user_name}.txt")
            if os.path.exists(set_file):
                os.remove(set_file)

            # 删除用户记忆文件
            memory_file = os.path.join("memories", f"{user_name}.txt")
            if os.path.exists(memory_file):
                os.remove(memory_file)

            # 删除用户资源目录
            user_resource_dir = os.path.join("resources", "images", user_name)
            if os.path.exists(user_resource_dir):
                shutil.rmtree(user_resource_dir)
        except Exception as e:
            print(f"删除用户文件时出错: {e}")

    def set_current_user(self, listbox):
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个用户")
            return

        user_name = listbox.get(selection[0])
        self.user.set(user_name)
        self.core.user_set(user_name)
        messagebox.showinfo("成功", f"当前用户已设置为 {user_name}")

    def browse_path(self, entry_widget, path_type):
        path = filedialog.askdirectory() if path_type != "file" else filedialog.askopenfilename()
        if path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, path)

    def save_settings(self, llm_path, sd_path, tts_path, cache_path, model, l2d_model):
        try:
            # 保存路径设置
            if llm_path and llm_path != self.core.llm_path:
                self.core.set_llm_path(llm_path)

            if sd_path and sd_path != self.core.sd_path:
                self.core.set_sd_path(sd_path)

            if tts_path and tts_path != self.core.tts_path:
                self.core.set_tts_path(tts_path)

            if cache_path and cache_path != self.core.cache_path:
                self.core.set_cache_set(cache_path)

            # 保存模型设置
            if model and model != self.core.model:
                self.core.llm_model_set(model)

            # 保存Live2D模型设置
            if l2d_model and l2d_model != self.core.l2d_model:
                # 注意：core.py中没有直接设置l2d_model的方法，需要通过配置管理
                from config_manager import save_config
                save_config("l2d_model", l2d_model)
                self.core.l2d_model = l2d_model

            self.log_message("Settings saved successfully")
            self.update_labels()
            self.update_tk()
        except Exception as e:
            self.log_message(f"Error saving settings: {e}")

    def reset_settings(self, llm_entry, sd_entry, tts_entry, cache_entry, model_entry, l2d_entry):
        llm_entry.delete(0, tk.END)
        llm_entry.insert(0, self.core.llm_path)
        sd_entry.delete(0, tk.END)
        sd_entry.insert(0, self.core.sd_path)
        tts_entry.delete(0, tk.END)
        tts_entry.insert(0, self.core.tts_path)
        cache_entry.delete(0, tk.END)
        cache_entry.insert(0, self.core.cache_path)
        model_entry.delete(0, tk.END)
        model_entry.insert(0, self.core.model)
        l2d_entry.delete(0, tk.END)
        l2d_entry.insert(0, self.core.l2d_model)

    def log_message(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.update()

    def mainloop(self):
        self.win.mainloop()

    def update_title(self):
        running_status = "Running" if self.core.get_info().get('running') else "Stopped"
        self.win.title(f"WeChatBotGUI - {running_status}")
        self.win.update()


app = App()
app.mainloop()
