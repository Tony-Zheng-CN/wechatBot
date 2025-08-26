import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
import time
import shutil

import requests
from PIL import Image


class AddUserDialog(tk.Toplevel):
    def __init__(self, image_path, set_path):
        super().__init__()
        self.title("添加用户")
        self.geometry("400x300")
        self.create_widgets()
        self.main_image_path = image_path
        self.set_path = set_path

    def create_widgets(self):
        self.username_label = ttk.Label(self, text="用户名:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        self.user_image_label = ttk.Label(self, text="用户头像:")
        self.user_image_label.grid(row=1, column=0, padx=5, pady=5)
        self.user_image_entry = ttk.Entry(self)
        self.user_image_entry.grid(row=1, column=1, padx=5, pady=5)
        self.user_image_button = ttk.Button(self, text="选择图片", command=self.select_image)
        self.user_image_button.grid(row=1, column=2, padx=5, pady=5)
        self.user_name_label = ttk.Label(self, text="你的姓名:")
        self.user_name_label.grid(row=2, column=0, padx=5, pady=5)
        self.user_name_entry = ttk.Entry(self)
        self.user_name_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2)
        self.user_age_label = ttk.Label(self, text="你的年龄:")
        self.user_age_label.grid(row=3, column=0, padx=5, pady=5)
        self.user_age_entry = ttk.Entry(self)
        self.user_age_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2)
        self.user_gender_label = ttk.Label(self, text="你的性别:")
        self.user_gender_label.grid(row=4, column=0, padx=5, pady=5)
        self.user_gender_entry = ttk.Entry(self)
        self.user_gender_entry.grid(row=4, column=1, padx=5, pady=5, columnspan=2)
        self.user_personality_label = ttk.Label(self, text="你的性格:")
        self.user_personality_label.grid(row=5, column=0, padx=5, pady=5)
        self.user_personality_entry = ttk.Entry(self)
        self.user_personality_entry.grid(row=5, column=1, padx=5, pady=5, columnspan=2)
        self.user_hobbies_label = ttk.Label(self, text="你的爱好:")
        self.user_hobbies_label.grid(row=6, column=0, padx=5, pady=5)
        self.user_hobbies_entry = ttk.Entry(self)
        self.user_hobbies_entry.grid(row=6, column=1, padx=5, pady=5, columnspan=2)
        self.user_background_label = ttk.Label(self, text="你的背景:")
        self.user_background_label.grid(row=7, column=0, padx=5, pady=5)
        self.user_background_entry = ttk.Entry(self)
        self.user_background_entry.grid(row=7, column=1, padx=5, pady=5, columnspan=2)
        self.enter_button = ttk.Button(self, text="确定", command=self.add_user)
        self.enter_button.grid(row=8, column=1, columnspan=3, padx=5, pady=5)

    def add_user(self):
        name = "郑若玲"
        age = "13岁"
        gender = "女"
        personality = "温柔，小公举性格，偶尔毒舌但超可爱，兄控"
        appearance = "圆脸，齐刘海，大眼睛，身高153cm，体重42kg"
        hobbies = "追番、画画、听可爱系音乐、刷B站"
        background_desc = "沉迷二次元番剧，宅，可爱系，绘画各种可爱的插画，有时会画一些有点黄的，B站ID:一只若玲酱"
        watched_anime = "《别当哥哥了》，《孤独摇滚！》，《某超科学的电磁炮》"

        user_name = "XXX"
        user_age = "14岁"
        user_gender = "男"
        user_personality = "萝莉控"
        user_hobbies = "追番"
        user_background = "沉迷二次元番剧"

        if self.user_name_entry.get() != "":
            user_name = self.user_name_entry.get()
        if self.user_age_entry.get() != "":
            user_age = self.user_age_entry.get()
        if self.user_gender_entry.get() != "":
            user_gender = self.user_gender_entry.get()
        if self.user_personality_entry.get() != "":
            user_personality = self.user_personality_entry.get()
        if self.user_hobbies_entry.get() != "":
            user_hobbies = self.user_hobbies_entry.get()
        if self.user_background_entry.get() != "":
            user_background = self.user_background_entry.get()
        self.set_path = os.path.join(self.set_path, f"{user_name}.txt")
        self.output_path = str(os.path.join(self.main_image_path, user_name))
        self.image_path = os.path.join(self.output_path, "image.png")
        self.mark_path = os.path.join(self.output_path, "mark.png")
        self.touch_path = os.path.join(self.output_path, "touch_head.png")
        self.chosen_path = os.path.join(self.output_path, "chosen.png")
        template = f"""# 人物档案
        你的名字：{name}
        你的年龄：{age}
        你的性别：{gender}
        你的性格：{personality}
        你的外貌：{appearance}
        你的兴趣爱好：{hobbies}
        你的背景设定：{background_desc}
        你看过的番剧：{watched_anime}

        用户的名字：{user_name}
        用户的年龄：{user_age}
        用户的性别：{user_gender}
        用户的性格：{user_personality}
        用户的兴趣爱好：{user_hobbies}
        用户的背景设定：{user_background}
        """
        if os.path.exists(self.output_path):
            if messagebox.askyesno("提示", "是否覆盖？"):
                shutil.rmtree(self.output_path)
            else:
                return False
        os.mkdir(self.output_path)
        self.generate_image()
        self.generate_mark()
        self.generate_touch()
        self.generate_chosen()
        with open(self.set_path, "w", encoding="utf-8") as f:
            f.write(template)
        self.destroy()

    def generate_image(self):
        avatar = Image.open(self.user_image_entry.get())
        resized_avatar = avatar.resize((50, 50), Image.Resampling.LANCZOS)
        resized_avatar.save(self.image_path)

    # 2. 生成 mark.png: 背景 + 用户头像部分 + 未读标记
    def generate_mark(self):
        # 创建背景图像 (32x32)
        background = Image.new("RGB", (32, 32), "#EBE9E8")

        # 打开并裁剪用户头像的右上角 16x16 部分
        avatar = Image.open(self.image_path)
        cropped_avatar = avatar.crop((50 - 27, 0, 50, 22))  # 右上角 16x16

        # 将裁剪后的头像粘贴到背景的右下角
        background.paste(cropped_avatar, (0, 10))

        # 加载并粘贴 unread_mark.png 到顶部居中
        unread_mark_path = str(os.path.join(self.main_image_path, "unread_mark.png"))  # 替换为实际的 unread_mark.png 路径
        unread_mark = Image.open(unread_mark_path).convert("RGBA")
        unread_mark = unread_mark.resize((16, 16), Image.Resampling.LANCZOS)  # 假设 unread_mark.png 是 16x16
        background.paste(unread_mark, (16, 0), unread_mark)  # 居中粘贴

        background.save(self.mark_path)

    def generate_chosen(self):
        # 创建背景图像 (32x32)
        background = Image.new("RGB", (60, 60), "#C8C8CA")

        # 打开并裁剪用户头像的右上角 16x16 部分
        avatar = Image.open(self.image_path)

        # 将裁剪后的头像粘贴到背景的右下角
        background.paste(avatar, (5, 5))

        background.save(self.chosen_path)

    # 3. 生成 touch_head.png: 背景 + 缩放后的用户头像
    def generate_touch(self):
        # 打开背景图像
        touch_head_background_path = str(
            os.path.join(self.main_image_path, "touch_head.png"))  # 替换为实际的 touch_head.png 路径
        background = Image.open(touch_head_background_path)

        # 打开用户头像并缩放为 42x40
        avatar = Image.open(self.image_path)
        resized_avatar = avatar.resize((42, 40), Image.Resampling.LANCZOS)

        # 粘贴到右侧最上方
        background.paste(resized_avatar, (background.width - resized_avatar.width, 0))

        background.save(self.touch_path)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.user_image_entry.delete(0, tk.END)
            self.user_image_entry.insert(0, file_path)


class WeChatBotGUI(tk.Tk):
    def __init__(self, main_module):
        super().__init__()
        self.main = main_module
        self.title("微信机器人")
        self.geometry("800x500")  # 减小窗口尺寸
        self.is_running = False
        self.user = ""
        self.create_widgets()

    def create_widgets(self):
        # 创建菜单栏
        self.create_menu()

        # 创建主框架
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 左侧面板（输出文本）
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, width=70, height=20)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # 右侧面板（控制区域）- 精简版
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

        # 用户选择区域
        user_frame = ttk.LabelFrame(right_frame, text="用户")
        user_frame.pack(pady=5, fill=tk.X)

        self.user_var = tk.StringVar()
        self.user_combobox = ttk.Combobox(user_frame, textvariable=self.user_var, state="readonly", width=15)
        self.user_combobox.pack(pady=2, padx=2, fill=tk.X)

        # 模型设置区域
        model_frame = ttk.LabelFrame(right_frame, text="模型")
        model_frame.pack(pady=5, fill=tk.X)

        self.model_var = tk.StringVar()
        self.model_combobox = ttk.Combobox(model_frame, textvariable=self.model_var, state="readonly", width=15)
        self.model_combobox.pack(pady=2, padx=2, fill=tk.X)

        # 控制按钮区域
        control_frame = ttk.Frame(right_frame)
        control_frame.pack(pady=10, fill=tk.X)

        self.start_button = ttk.Button(control_frame, text="开始", command=self.toggle_run)
        self.start_button.pack(pady=2, padx=2, fill=tk.X)

        # 状态区域
        status_frame = ttk.Frame(right_frame)
        status_frame.pack(pady=5, fill=tk.X)

        self.debug_var = tk.BooleanVar(value=self.main.debug)
        self.tts_var = tk.BooleanVar(value=self.main.tts)

        ttk.Checkbutton(status_frame, text="调试", variable=self.debug_var, command=self.toggle_debug).pack(pady=1,
                                                                                                           padx=2,
                                                                                                           anchor=tk.W)
        ttk.Checkbutton(status_frame, text="TTS", variable=self.tts_var, command=self.toggle_tts).pack(pady=1,
                                                                                                       padx=2,
                                                                                                       anchor=tk.W)

        self.model_combobox.bind("<<ComboboxSelected>>", self.change_model)
        self.user_combobox.bind("<<ComboboxSelected>>", self.set_user)

        self.update_user_list()
        self.update_model_list()

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # 用户菜单
        user_menu = tk.Menu(menubar, tearoff=0)
        user_menu.add_command(label="添加用户", command=self.add_user)
        user_menu.add_command(label="删除用户", command=self.delete_user)
        user_menu.add_separator()
        user_menu.add_command(label="管理记忆", command=self.manage_memory)
        user_menu.add_command(label="删除记忆", command=self.delete_memory)
        user_menu.add_separator()
        user_menu.add_command(label="列出所有用户", command=self.list_users)
        menubar.add_cascade(label="用户", menu=user_menu)

        # 模型菜单
        model_menu = tk.Menu(menubar, tearoff=0)
        model_menu.add_command(label="模型列表", command=self.show_model_list)
        menubar.add_cascade(label="模型", menu=model_menu)

        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="清除缓存", command=self.clear_cache)
        tools_menu.add_command(label="设置缓存路径", command=self.set_cache_path)
        tools_menu.add_separator()
        tools_menu.add_command(label="切换调试模式", command=self.toggle_debug)
        tools_menu.add_command(label="切换语音合成", command=self.toggle_tts)
        menubar.add_cascade(label="工具", menu=tools_menu)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        help_menu.add_command(label="帮助", command=self.show_help)
        menubar.add_cascade(label="帮助", menu=help_menu)

    def update_user_list(self):
        if os.path.exists("set"):
            users = [os.path.splitext(f)[0] for f in os.listdir("set") if os.path.isfile(os.path.join("set", f))]
            self.user_combobox['values'] = users
            if users:
                self.user_combobox.current(0)
        else:
            self.user_combobox['values'] = []

    def update_model_list(self):
        try:
            if self.main.launcher == "ollama":
                self.model_combobox['values'] = self.main.olML()
            else:
                self.model_combobox['values'] = self.main.fcML()
            if self.model_combobox['values']:
                self.model_combobox.set(self.main.model)
        except Exception as e:
            self.log(f"获取模型列表失败: {e}")

    def log(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)

    def set_user(self, event):
        if self.user_combobox.get():
            self.user = self.user_combobox.get()
            self.main.set_name(self.user)
            self.log(f"用户设置为: {self.user}")
        else:
            messagebox.showwarning("警告", "请选择一个用户")

    def add_user(self):
        try:
            user = AddUserDialog(image_path="resources\\images\\", set_path="set\\")
            self.wait_window(user)
            self.update_user_list()
            self.log(f"用户添加成功")
        except Exception as e:
            messagebox.showerror("错误", f"添加用户失败: {e}")

    def delete_user(self):
        if not self.user_combobox.get():
            messagebox.showwarning("警告", "请选择要删除的用户")
            return

        if messagebox.askyesno("确认", f"确定要删除用户 {self.user_combobox.get()} 吗?"):
            try:
                user = self.user_combobox.get()
                if os.path.exists(f"memories\\{user}.txt"):
                    os.remove(f"memories\\{user}.txt")
                if os.path.exists(f"set\\{user}.txt"):
                    os.remove(f"set\\{user}.txt")
                if os.path.exists(f"resources\\{user}"):
                    shutil.rmtree(f"resources\\{user}")
                self.update_user_list()
                self.log(f"用户 {user} 删除成功")
            except Exception as e:
                messagebox.showerror("错误", f"删除用户失败: {e}")

    def manage_memory(self):
        if not self.user_combobox.get():
            messagebox.showwarning("警告", "请选择用户")
            return

        user = self.user_combobox.get()
        if not os.path.exists(f"memories\\{user}.txt"):
            messagebox.showinfo("信息", "当前用户没有长期记忆")
            return

        memory_content = open(f"memories\\{user}.txt", "r", encoding="utf-8").read()
        memory_window = tk.Toplevel(self)
        memory_window.title(f"{user} 的记忆")
        memory_window.geometry("600x400")

        text = scrolledtext.ScrolledText(memory_window, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True)
        text.insert(tk.END, memory_content)

        def save_memory():
            with open(f"memories\\{user}.txt", "w", encoding="utf-8") as f:
                f.write(text.get(1.0, tk.END))
            messagebox.showinfo("信息", "记忆已保存")

        ttk.Button(memory_window, text="保存记忆", command=save_memory).pack(pady=5)

    def list_users(self):
        if os.path.exists("set"):
            users = [os.path.splitext(f)[0] for f in os.listdir("set") if os.path.isfile(os.path.join("set", f))]
            if users:
                self.log("用户列表: " + ", ".join(users))
            else:
                self.log("暂无用户")
        else:
            self.log("用户目录不存在")

    def change_model(self, event):
        if self.model_combobox.get():
            new_model = self.model_combobox.get()
            if new_model in self.model_combobox['values']:
                self.main.model = new_model
                self.main.save_config(self.main.cache_path, self.main.model, self.main.tts, self.main.debug,
                                      self.main.launcher, getattr(self.main, 'enable_draw', False))
                self.log(f"模型已切换为: {new_model}")
            else:
                messagebox.showwarning("警告", f"模型 {new_model} 不存在")
        else:
            messagebox.showwarning("警告", "请选择模型")

    def show_model_list(self):
        try:
            if self.main.launcher == "ollama":
                model_list = self.main.olML()
            else:
                model_list = self.main.fcML()
            self.log(f"模型列表: {model_list}")
        except Exception as e:
            self.log(f"获取模型列表失败: {e}")

    def clear_cache(self):
        try:
            self.main.clear_cache()
            self.log("缓存已清空")
        except Exception as e:
            self.log(f"清空缓存失败: {e}")

    def toggle_debug(self):
        self.main.debug = self.debug_var.get()
        self.main.save_config(self.main.cache_path, self.main.model, self.main.tts, self.main.debug, self.main.launcher, getattr(self.main, 'enable_draw', False))
        self.log(f"调试模式: {'开启' if self.main.debug else '关闭'}")

    def toggle_tts(self):
        self.main.tts = self.tts_var.get()
        self.main.save_config(self.main.cache_path, self.main.model, self.main.tts, self.main.debug, self.main.launcher, getattr(self.main, 'enable_draw', False))
        self.log(f"语音合成: {'开启' if self.main.tts else '关闭'}")

    def set_cache_path(self):
        path = tk.filedialog.askdirectory(initialdir=self.main.cache_path)
        if path:
            self.main.set_cache_dir(path)
            self.main.save_config(path, self.main.model, self.main.tts, self.main.debug, self.main.launcher, getattr(self.main, 'enable_draw', False))
            self.log(f"缓存路径已设置为: {path}")

    def show_about(self):
        messagebox.showinfo("关于", "微信机器人 v1.0\n基于main.py构建的GUI界面")

    def show_help(self):
        messagebox.showinfo("帮助", "请参考main.py中的help.txt文件")

    def toggle_run(self):
        if not self.user_combobox.get():
            messagebox.showwarning("警告", "请先设置用户")
            return

        self.is_running = not self.is_running
        self.start_button.config(text="停止" if self.is_running else "开始")
        self.user = self.user_combobox.get()
        self.main.set_name(self.user)

        if self.is_running:
            self.log("开始运行...")
            self.run_thread = threading.Thread(target=self.run_bot)
            self.run_thread.start()

    def delete_memory(self):
        user = self.user_combobox.get()
        if not user:
            messagebox.showwarning("警告", "请先选择用户")
            return

        memory_path = f"memories\\{user}.txt"
        if not os.path.exists(memory_path):
            messagebox.showinfo("提示", f"用户 {user} 没有记忆文件")
            return

        if messagebox.askyesno("确认", f"确定要删除用户 {user} 的记忆吗？"):
            try:
                os.remove(memory_path)
                self.log(f"用户 {user} 的记忆已删除")
                messagebox.showinfo("成功", f"用户 {user} 的记忆已删除")
            except Exception as e:
                messagebox.showerror("错误", f"删除记忆失败：{e}")

    def run_bot(self):
        try:
            stop_flag = False
            self.main.activate_wechat_window()
            place = self.main.click_user()
            self.log(f"模型: {self.main.model}\n运行器: {self.main.launcher}")

            if place:
                if self.main.debug:
                    self.main.send_message(f"[DEBUG]{self.main.model}已接入")
                self.main.clear_cache()
                self.main.click_user_next()

                if self.main.launcher == "fastchat":
                    ai_agent = self.main.fcAIAgent(user_name=self.user)
                elif self.main.launcher == "ollama":
                    ai_agent = self.main.olAIAgent(user_name=self.user, model=self.main.model)

                while self.is_running and not stop_flag:
                    place = self.main.check_unread_message()
                    if place:
                        self.main.pag.click(x=place[0] + 30, y=place[1] + 20)
                        new_message = self.main.get_new_message()

                        if not new_message:
                            self.main.click_user_next()
                            continue

                        message_type = new_message[0]
                        if self.main.debug:
                            self.log(f"[DEBUG]新消息: {new_message}")

                        if new_message[0]:
                            if new_message[0] == "text":
                                new_message = new_message[1]
                                if new_message.startswith("#"):
                                    if new_message.split(" ")[0] == "#call":
                                        type_text = new_message.split(" ")[1]
                                        if type_text == "sound":
                                            self.main.call_sound()
                                            if self.main.debug:
                                                self.log("[DEBUG]sound call")
                                        elif type_text == "video":
                                            self.main.call_video()
                                            if self.main.debug:
                                                self.log("[DEBUG]video call")
                                    elif new_message.split(" ")[0] == "#open":
                                        type_text = new_message.split(" ")[1]
                                        message_text = new_message.split(" ")[2]
                                        if type_text == "web":
                                            self.main.send_message(f"已经在哥哥的电脑上打开：{message_text}")
                                            self.main.open_web(message_text)
                                            if self.main.debug:
                                                self.log(f"[DEBUG]open website{message_text}")
                                    elif new_message.split(" ")[0] == "#draw":
                                        self.main.send_message("正在绘画...")
                                        prompt = new_message.split(" ")[1]
                                        self.log(f"[DEBUG]绘画提示词: {prompt}")
                                        self.main.send_message("正在绘画...")
                                        self.main.send_file(self.main.sd_api(new_message.split(" ")[1]))
                                        if self.debug_var.get():
                                            self.log(f"[DEBUG]sd draw.prompt{new_message.split(' ')[1]}")
                                elif new_message.startswith("/"):
                                    if new_message == "/exit":
                                        self.is_running = False
                                    elif new_message == "/help":
                                        self.main.send_message(self.main.help_text)
                                        self.log("[DEBUG]显示帮助信息")
                                    elif new_message == "/tts":
                                        self.main.tts = not self.main.tts
                                        self.tts_var.set(self.main.tts)
                                        if self.main.debug:
                                            self.main.send_message(f"[DEBUG]TTS:{self.main.tts}")
                                            self.log(f"[DEBUG]TTS状态: {self.main.tts}")
                                        self.main.save_config(self.main.cache_path, self.main.model, self.main.tts,
                                                              self.main.debug, self.main.launcher,
                                                              self.main.enable_draw)
                                    elif new_message == "/tts_status":
                                        self.main.send_message(f"TTS:{self.main.tts}")
                                        self.log(f"[DEBUG]TTS状态: {self.main.tts}")
                                    elif new_message == "/debug":
                                        self.main.debug = not self.main.debug
                                        self.debug_var.set(self.main.debug)
                                        if self.main.debug:
                                            self.main.send_message(f"[DEBUG]debug:{self.main.tts}")
                                            self.log(f"[DEBUG]调试模式开启")
                                        self.main.save_config(self.main.cache_path, self.main.model, self.main.tts,
                                                              self.main.debug, self.main.launcher,
                                                              self.main.enable_draw)
                                    elif new_message == "/shutdown":
                                        self.main.send_message("哥哥你的电脑报废了...")
                                        os.system("shutdown -s -t 0")
                                    elif new_message.startswith("/file"):
                                        try:
                                            message_text = new_message.split(" ")[1]
                                        except IndexError:
                                            message_text = ""
                                        if self.main.debug:
                                            self.main.send_message("[DEBUG]正在发送文件...")
                                            self.log(f"[DEBUG]发送文件: {message_text}")
                                        self.main.send_file(message_text)
                                    elif new_message.startswith("/dir"):
                                        try:
                                            message_text = new_message.split(" ")[1]
                                        except IndexError:
                                            message_text = ""
                                        if self.main.debug:
                                            self.main.send_message("[DEBUG]正在发送文件夹目录...")
                                            self.log(f"[DEBUG]发送目录: {message_text}")
                                        self.main.send_dir(message_text)
                                    elif new_message == "/reset":
                                        os.remove(f"memories\\{self.user}.txt")
                                        if self.main.debug:
                                            self.main.send_message("[DEBUG]记忆已重置")
                                            self.log(f"[DEBUG]用户 {self.user} 的记忆已重置")
                                    elif new_message.startswith("/model"):
                                        if self.main.launcher == "ollama":
                                            model_list = self.main.olML()
                                        else:
                                            model_list = self.main.fcML()
                                        parts = new_message.split(" ")
                                        if len(parts) < 2:
                                            self.main.send_message("模型命令格式错误")
                                            continue

                                        if parts[1] == "list":
                                            self.log(f"[DEBUG]模型列表: {model_list}")
                                            self.main.send_message(str(model_list))
                                        elif parts[1] == "set" and len(parts) >= 3:
                                            new_model = parts[2]
                                            if new_model in model_list:
                                                self.main.model = new_model
                                                self.main.send_message(f"已切换模型为{self.main.model}")
                                                self.log(f"[DEBUG]模型已切换为: {self.main.model}")
                                                self.main.save_config(self.main.cache_path, self.main.model,
                                                                      self.main.tts,
                                                                      self.main.debug, self.main.launcher,
                                                                      self.main.enable_draw)
                                                self.update_model_list()
                                            else:
                                                self.main.send_message(f"无名为{new_model}的模型")
                                                self.log(f"[WARN]模型不存在: {new_model}")
                                        else:
                                            self.main.send_message(f"未知命令: {new_message}")
                                            self.log(f"[WARN]未知命令: {new_message}")
                                else:
                                    self.main.send_message("少女思考中...")
                                    # 创建一个事件用于控制AI思考过程是否被中断
                                    interrupt_event = threading.Event()

                                    # 使用线程来处理AI回复，这样可以在主线程中检查新消息
                                    def get_ai_response(result_container):
                                        try:
                                            result_container['response'] = ai_agent.get_response(
                                                (message_type, new_message))
                                        except Exception as e:
                                            result_container['response'] = "呜呜~思考过程中断了啦！"
                                            self.log(f"[ERROR] AI response error: {e}")

                                    result = {}
                                    ai_thread = threading.Thread(target=get_ai_response, args=(result,))
                                    ai_thread.start()

                                    # 在AI思考过程中检查是否有新消息
                                    while ai_thread.is_alive():
                                        time.sleep(0.1)  # 短暂休眠以避免过度占用CPU
                                        place = self.main.check_unread_message()
                                        if place:
                                            # 有新消息，中断当前思考
                                            interrupt_event.set()
                                            ai_thread.join(timeout=1)  # 等待线程结束，最多等待1秒

                                            # 处理新消息
                                            self.main.pag.click(x=place[0] + 30, y=place[1] + 20)
                                            new_msg = self.main.get_new_message()
                                            msg_type = new_msg[0]
                                            if new_msg[0]:
                                                if new_msg[0] == "text":
                                                    msg_content = new_msg[1]
                                                    # 将新消息加入AI的上下文
                                                    if self.main.launcher == "fastchat":
                                                        ai_agent.messages.append(
                                                            {"role": "user", "content": msg_content})
                                                    elif self.main.launcher == "ollama":
                                                        ai_agent.message.append(
                                                            {"role": "user", "content": msg_content})
                                                        ai_agent.memory_manager.save_memory(f"[user] {msg_content}")

                                                    if self.main.debug:
                                                        self.log(f"[DEBUG] Interrupted by new message: {msg_content}")
                                            # 重新开始检查消息循环
                                            break

                                    # 如果思考未被中断，则继续处理原消息的回复
                                    if not interrupt_event.is_set():
                                        ai_thread.join()  # 等待AI思考完成
                                        reply = result.get('response', "呜呜~我没有想好要说什么...")

                                        if self.main.debug:
                                            self.log(f"[DEBUG]Ollama响应: {reply}")

                                        if self.main.enable_draw:
                                            if "你要看" in reply and "画" in reply:
                                                try:
                                                    sd_prompt = ai_agent.get_response(
                                                        f"从{reply}中提取适用于SD的AI绘画提示词，英语，具体，500词以内。只有单词或短语",
                                                        memory=False)
                                                    self.main.send_message("正在绘画...")
                                                    prompt = new_message.split(" ")[1]
                                                    self.log(f"[DEBUG]绘画提示词: {prompt}")
                                                    self.main.send_message("正在绘画...")
                                                    self.main.send_file(self.main.sd_api(new_message.split(" ")[1]))
                                                    if self.debug_var.get():
                                                        self.log(f"[DEBUG]sd draw.prompt{new_message.split(' ')[1]}")
                                                    time.sleep(0.2)
                                                except Exception as e:
                                                    self.main.send_message("绘画失败")
                                                    self.log(f"[WARN]绘画错误: {e}")

                                        if "//call video" in reply:
                                            reply = reply.replace("//call video", "")
                                            self.main.call_video()
                                            if self.main.debug:
                                                self.log(f"[DEBUG]调用视频")
                                            time.sleep(0.2)

                                        if "//touch_head" in reply:
                                            self.main.head_shot()
                                            if self.main.debug:
                                                self.log(f"[DEBUG]触摸头部")
                                            reply = reply.replace("//touch_head", "")
                                            time.sleep(0.2)

                                        if self.main.tts:
                                            try:
                                                if self.debug_var.get():
                                                    self.log(f"[DEBUG]tts start.")
                                                self.main.send_message("TTS...")
                                                res = requests.post(self.main.tts_path, data={
                                                    "text": reply,
                                                    "prompt": "",
                                                    "voice": "3333",
                                                    "temperature": 0.3,
                                                    "top_p": 0.7,
                                                    "top_k": 20,
                                                    "skip_refine": 0,
                                                    "custom_voice": 0
                                                })
                                                if self.debug_var.get():
                                                    self.log(f"[DEBUG]TTS file path:{res.json()['filename']}")
                                                try:
                                                    self.main.send_file(res.json()["filename"])
                                                except requests.exceptions.JSONDecodeError as e:
                                                    self.log(f"Failed to decode JSON response from TTS service: {e}")
                                            except Exception as e:
                                                if self.debug_var.get():
                                                    self.log(f"[DEBUG]Error occurred while sending TTS request: {e}")
                                                self.main.send_message("哥哥！是不是你把我的声带偷了！！！：" + str(e))

                                        self.main.send_message(reply)
                                        self.main.call_times -= 0.1

                                self.main.click_user_next()
                        else:
                            self.main.click_user_next()
                    time.sleep(1)  # 模拟检查间隔
        except Exception as e:
            self.log(f"运行错误: {e}")
        finally:
            self.is_running = False
            self.start_button.config(text="开始")
            self.log("运行结束")


if __name__ == "__main__":
    import main as main_module

    app = WeChatBotGUI(main_module)
    app.mainloop()
