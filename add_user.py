from PIL import Image
import os
import shutil


class NewUser:
    def __init__(self, user_name, user_avatar_path, image_path, set_path):
        self.user_name = user_name
        self.user_avatar_path = user_avatar_path
        self.main_image_path = image_path
        self.set_path = os.path.join(set_path, f"{self.user_name}.txt")
        self.output_path = str(os.path.join(self.main_image_path, self.user_name))
        self.image_path = os.path.join(self.output_path, "image.png")
        self.mark_path = os.path.join(self.output_path, "mark.png")
        self.touch_path = os.path.join(self.output_path, "touch_head.png")
        self.chosen_path = os.path.join(self.output_path, "chosen.png")
        if os.path.exists(self.output_path):
            if input(f"{self.output_path}已存在文件夹，是否覆盖(y/n)") == "y":
                shutil.rmtree(self.output_path)
                os.mkdir(self.output_path)
            else:
                return

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
        print("正在为您创建角色设定，请按提示填写：")
        name = "郑若玲"
        age = "13岁"
        gender = "女"
        personality = "温柔，小公举性格，偶尔毒舌但超可爱，兄控"
        appearance = "圆脸，齐刘海，大眼睛，身高153cm，体重42kg"
        hobbies = "追番、画画、听可爱系音乐、刷B站"
        background_desc = "沉迷二次元番剧，宅，可爱系，绘画各种可爱的插画，有时会画一些有点黄的，B站ID:一只若玲酱"
        watched_anime = "《别当哥哥了》，《孤独摇滚！》，《某超科学的电磁炮》"

        user_name = input("用户的姓名（默认：XXX）：") or "XXX"
        user_age = input("用户的年龄（默认：14岁）：") or "14岁"
        user_gender = input("用户的性别（默认：男）：") or "男"
        user_personality = input("用户性格（默认：萝莉控）：") or "萝莉控"
        user_hobbies = input("用户兴趣爱好（默认：追番）：") or "追番"
        user_background = input("用户背景设定（默认：沉迷二次元番剧") or "沉迷二次元番剧"

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
        with open(self.set_path, "w", encoding="utf-8") as f:
            f.write(template)


def add_user(username=None, image_dir="resources\\images\\", set_path="set\\"):
    if not username:
        username = input("请输入用户名：")
    avatar_path = input("请输入用户头像图片路径：")
    new_user = NewUser(username, avatar_path, image_dir, set_path)
    new_user.generate_image()
    new_user.generate_mark()
    new_user.generate_touch()
    new_user.generate_chosen()
    new_user.add_set()
    print(f"用户 {username} 已成功创建！")

if __name__ == '__main__':
    add_user()
