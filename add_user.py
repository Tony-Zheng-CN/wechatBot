import json

from PIL import Image
import os
import shutil


class NewUser:
    def __init__(self, user_info, exists_cover=True):
        self.user_info = user_info
        self.user_name = self.user_info.get("username", None)
        if not self.user_name:
            raise ValueError("User name is empty")
        self.user_avatar_path = self.user_info.get("avatar_path", None)
        self.main_image_path = self.user_info.get("image_dir", "images\\")
        self.set_path = os.path.join(self.user_info.get("set_path", "set\\"), f"{self.user_name}.txt")
        self.output_path = str(os.path.join(self.main_image_path, self.user_name))
        self.image_path = os.path.join(self.output_path, "image.png")
        self.mark_path = os.path.join(self.output_path, "mark.png")
        self.touch_path = os.path.join(self.output_path, "touch_head.png")
        self.chosen_path = os.path.join(self.output_path, "chosen.png")
        if os.path.exists(self.output_path):
            if exists_cover:
                shutil.rmtree(self.output_path)
                os.mkdir(self.output_path)
            else:
                raise FileExistsError("User already exists")

    def generate_image(self):
        avatar = Image.open(self.user_avatar_path)
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
        background.paste(resized_avatar, (background.width - resized_avatar.width, 0), resized_avatar)

        background.save(self.touch_path)

    def add_set(self):
        ai_set = json.loads(os.path.join("resources", "ai_set.txt"), encoding="utf-8")
        name = ai_set.get("name", "郑若玲")
        age = ai_set.get("age", "13")
        gender = ai_set.get("sex", "女")
        personality = ai_set.get("personality", "温柔，小公举性格，偶尔毒舌但超可爱，兄控")
        appearance = ai_set.get("appearance", "圆脸，齐刘海，大眼睛，身高153cm，体重42kg")
        hobbies = ai_set.get("hobby", "追番、画画、听可爱系音乐、刷B站")
        background = ai_set.get("background", "沉迷二次元番剧，宅，可爱系，绘画各种可爱的插画，有时会画一些有点黄的，B站ID:一只若玲酱")

        user_name = self.user_info.get("name", "张三")
        user_age = self.user_info.get("age", "14")
        user_gender = self.user_info.get("sex", "男")
        user_personality = self.user_info.get("personality", "可爱的物品")
        user_hobbies = self.user_info.get("hobby", "看番")
        user_background = self.user_info.get("background", "初中生")

        template = f"""# 人物档案
你的名字：{name}
你的年龄：{age}岁
你的性别：{gender}
你的性格：{personality}
你的外貌：{appearance}
你的兴趣爱好：{hobbies}
你的背景设定：{background}

用户的名字：{user_name}
用户的年龄：{user_age}岁
用户的性别：{user_gender}
用户的性格：{user_personality}
用户的兴趣爱好：{user_hobbies}
用户的背景设定：{user_background}
"""
        with open(self.set_path, "w", encoding="utf-8") as f:
            f.write(template)


def add_user(user_info):
    new_user = NewUser(user_info)
    new_user.generate_image()
    new_user.generate_mark()
    new_user.generate_touch()
    new_user.generate_chosen()
    new_user.add_set()
    return True
