import time
import shutil
import pandas.io.clipboard as cb
import pyautogui as pag
import webbrowser
import os
import logging
import win32gui
import l2d_agent.live2d_control as l2d

logger_gc = logging.getLogger("gui_control")
logger_gc_formatter = logging.Formatter("[%(levelname)s][%(name)s]%(message)s")

image_dir = f'{os.getcwd()}\\resources\\images\\'
cache_dir = f'{os.getcwd()}\\cache\\'

name = 'user'
debug = False


def set_debug_gc(debug_):
    global debug
    debug = debug_
    if debug:
        logger_gc.setLevel(logging.DEBUG)
    else:
        logger_gc.setLevel(logging.INFO)


def clear_cache():
    logger_gc.debug(f"Clear cache")
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)


def set_name(name_):
    global name
    if os.path.exists(f"set\\{name_}.txt") and os.path.exists(f"{image_dir}{name_}"):
        name = name_
        logger_gc.info(f"Set user name:{name}")
        return True
    else:
        print(f"{name_} 不存在")
        return False


def set_image_dir(dir_path):
    global image_dir
    logger_gc.debug(f"Set image dir:{image_dir}")
    image_dir = dir_path


def set_cache_dir(dir_path):
    global cache_dir
    logger_gc.debug(f"Set cache dir:{cache_dir}")
    cache_dir = dir_path


def get_contact_list_region():
    hwnd = win32gui.FindWindow(None, "微信")
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    try:
        title_location = pag.locateOnScreen(f'{image_dir}wechat_title.png', confidence=0.8)
        contact_list_region = (int(title_location.left), int(title_location.top+title_location.height),
                               int(title_location.left + title_location.width),
                               int(bottom))
        logging.debug(f"Get contact list region:{contact_list_region}")
        return contact_list_region
    except pag.ImageNotFoundException:
        return False


# 模拟点击操作，用于激活微信窗口
def activate_wechat_window():
    logger_gc.debug(f"Activate wechat window.")
    # 根据实际屏幕截图查找微信图标或窗口位置，此处为示例坐标
    try:
        wechat_icon = pag.locateOnScreen(image_dir + 'wechat_icon.png', confidence=0.8)
        pag.click(wechat_icon.left + 25, wechat_icon.top + 15)
        return wechat_icon
    except pag.ImageNotFoundException:
        try:
            wechat_icon = pag.locateOnScreen(f'{image_dir}wechat_icon_mark.png', confidence=0.8)
            pag.click(wechat_icon.left + 25, wechat_icon.top + 15)
            return wechat_icon
        except pag.ImageNotFoundException:
            try:
                wechat_icon = pag.locateOnScreen(f'{image_dir}wechat_icon_unfilled.png', confidence=0.8)
                pag.click(wechat_icon.left + 25, wechat_icon.top + 15)
                return wechat_icon
            except pag.ImageNotFoundException:
                try:
                    wechat_icon = pag.locateOnScreen(f'{image_dir}wechat_icon_unfilled_mark.png', confidence=0.8)
                    pag.click(wechat_icon.left + 25, wechat_icon.top + 15)
                    return wechat_icon
                except pag.ImageNotFoundException:
                    logger_gc.critical(f"Activate wechat window failed")
                    exit()


def click_user():
    logger_gc.debug(f"Activate user.")
    try:
        contact_location = pag.locateOnScreen(f'{image_dir}{name}/image.png', confidence=0.9, region=get_contact_list_region())
        pag.click(contact_location.left + 25, contact_location.top + 15)
        return contact_location
    except pag.ImageNotFoundException:
        try:
            contact_location = pag.locateOnScreen(f'{image_dir}{name}/mark.png', confidence=0.9, region=get_contact_list_region())
            pag.click(contact_location.left + 25, contact_location.top + 15)
            return contact_location
        except pag.ImageNotFoundException:
            logger_gc.warning(f"Activate user failed.")
            return False


def click_user_next():
    try:
        logger_gc.debug(f"Activate next user.")
        contact_location = pag.locateOnScreen(f'{image_dir}{name}/image.png', confidence=0.8, region=get_contact_list_region())
        pag.click(contact_location.left + 25, contact_location.top + 100)
        return contact_location
    except pag.ImageNotFoundException:
        try:
            contact_location = pag.locateOnScreen(f'{image_dir}{name}/mark.png', confidence=0.8, region=get_contact_list_region())
            pag.click(contact_location.left + 25, contact_location.top + 100)
            return contact_location
        except pag.ImageNotFoundException:
            logger_gc.debug(f"Activate next user.")
            return False


def check_contact():
    logger_gc.debug(f"Check contact.")
    try:
        pag.locateOnScreen(f'{image_dir}{name}\chosen.png', confidence=0.8, region=get_contact_list_region())
        return True
    except pag.ImageNotFoundException:
        return False


def check_unread_message():
    logger_gc.debug(f"Check unread message.")
    try:
        contact_location = pag.locateOnScreen(f'{image_dir}{name}/mark.png', confidence=0.9, region=get_contact_list_region())
        return contact_location
    except pag.ImageNotFoundException:
        return False


def call_sound():
    logger_gc.info("Sound call")
    if not check_contact():
        click_user()
    try:
        contact_location = pag.locateOnScreen(f'{image_dir}call_sound.png', confidence=0.9)
        pag.click(contact_location)
        return True
    except pag.ImageNotFoundException:
        return False


def call_video(l2d_model=None):
    logger_gc.info("Video call")
    if not check_contact():
        click_user()
    try:
        contact_location = pag.locateOnScreen(f'{image_dir}call_video.png', confidence=0.9)
        pag.click(contact_location)
    except pag.ImageNotFoundException:
        return False
    if l2d_model:
        l2d_obj = l2d.Live2d(l2d_model=l2d_model)
        l2d_obj.init()
        start_time = time.time()
        while time.time() - start_time < 10:
            l2d_model.set_action("hello")
            l2d_model.set_emotion("happy")
            for x in range(0, 100):
                l2d_model.update()
                time.sleep(0.01)
    return True

def open_web(web_url):
    logger_gc.debug(f"Open website:{web_url}")
    webbrowser.open(web_url)


def get_new_message():
    if not check_contact():
        click_user()
    try:
        screen_shut = pag.locateOnScreen(f'{image_dir}screen_shut.png', confidence=0.8)
    except pag.ImageNotFoundException:
        return False
    try:
        pag.moveTo(screen_shut.left - 10, screen_shut.top - 30)
        x, y = pag.position()
        rgb = pag.screenshot().getpixel((x, y))
        while rgb == (245, 245, 245):
            pag.moveTo(x, y - 10)
            x, y = pag.position()
            rgb = pag.screenshot().getpixel((x, y))
        pag.rightClick(x, y)
        time.sleep(0.1)
        try:
            pag.locateOnScreen(f'{image_dir}image_menu.png', confidence=0.6)
            pag.click(pag.position()[0], pag.position()[1])
            output = ("image", get_new_image())
        except pag.ImageNotFoundException:
            copy = pag.locateOnScreen(f'{image_dir}copy.png', confidence=0.6)
            pag.click(copy.left + 5, copy.top + 5)
            output = ("text", cb.paste())
        logger_gc.info(f"Get new message {output}.")
        return output
    except pag.ImageNotFoundException:
        return False


def get_new_image():
    time.sleep(0.1)
    pag.click(x=pag.position()[0], y=pag.position()[1] - 30)
    try:
        time.sleep(0.5)
        image_download = pag.locateOnScreen(f'{image_dir}image_download.png', confidence=0.8)
        pag.click(x=image_download[0], y=image_download[1])
        time.sleep(0.4)
        file_path = os.path.join(cache_dir, "user_input.jpg")
        if os.path.exists(file_path):
            os.remove(file_path)
        cb.copy(file_path)
        logger_gc.info(f"Get new image {file_path}.")
        pag.hotkey('ctrl', 'v')
        time.sleep(0.4)
        pag.press('enter')
        pag.hotkey("alt", "f4")
        return file_path
    except pag.ImageNotFoundException:
        return False


def head_shot():
    logger_gc.info(f"Touch head")
    if not check_contact():
        click_user()
    try:
        touch_icon = pag.locateOnScreen(f'{image_dir}{name}/touch_head.png', confidence=0.8)
        pag.rightClick(touch_icon.left + 100, touch_icon.top + 20)
    except pag.ImageNotFoundException:
        return False
    time.sleep(0.1)
    try:
        touch_icon = pag.locateOnScreen(f'{image_dir}go_to_head.png', confidence=0.8)
        pag.click(touch_icon.left + 20, touch_icon.top + 5)
        return True
    except pag.ImageNotFoundException:
        return False


def send_message(message):
    logger_gc.info(f"Send message:{message}.")
    if not check_contact():
        click_user()
    try:
        pag.click(x=int(pag.locateOnScreen(f"{image_dir}wechat_send_toolbar.png")[0]) + 20,
                  y=int(pag.locateOnScreen(f"{image_dir}wechat_send_toolbar.png")[1]) + 60)
    except pag.ImageNotFoundException:
        return False
    try:
        cb.copy(message)
        pag.hotkey('ctrl', 'v')
        pag.press('enter')
        return True
    except Exception as e:
        logger_gc.error(f"Send message failed.{e}")
        return False


def send_file(file_path):
    logger_gc.info(f"Send file:{file_path}.")
    if not check_contact():
        click_user()
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    if not os.path.exists(file_path):
        send_message(f"{name}，文件是不是被你吃了！")
        return False
    try:
        source_file = open(file_path, "rb")
        copy_file = open(f"{cache_dir}\\{os.path.basename(file_path)}", "wb")
        copy_file.write(source_file.read())
        source_file.close()
        copy_file.close()
    except Exception as e:
        send_message(f"{name}，文件是不是被你吃了！")
        logger_gc.error(f"Send file failed.{e}")
        return False
    file_path = f"{cache_dir}{os.path.basename(file_path)}"
    try:
        pag.click(x=int(pag.locateOnScreen(f"{image_dir}send_file.png")[0]),
                  y=int(pag.locateOnScreen(f"{image_dir}send_file.png")[1]))
        time.sleep(1)
        cb.copy(file_path)
        pag.hotkey('ctrl', 'v')
        time.sleep(0.1)
        pag.press('enter')
        time.sleep(0.4)
        pag.press('enter')
        return True
    except pag.ImageNotFoundException:
        return False


def send_dir(dir_path):
    logger_gc.info(f"Send dir:{dir_path}.")
    if not check_contact():
        click_user()
    if not os.path.exists(cache_dir):
        send_message(f"{name}，文件夹是不是被你吃了！")
        return False
    try:
        list_dir = os.listdir(dir_path)
        send_message(f"{name}，这是你最爱吃的文件夹：")
        send_message(f"{list_dir}")
        return True
    except Exception as e:
        send_message(f"{name}，文件夹是不是被你吃了！")
        logger_gc.warning(f"Send dir failed.{e}")
        return False


def click_log():
    try:
        wechat_relog_img = pag.locateCenterOnScreen(
            os.path.join(os.getcwd(), "resources", "images", "wechat_relogin_button.png"), confidence=0.8)
    except pag.ImageNotFoundException:
        return False
    pag.click(x=wechat_relog_img[0] + 10, y=wechat_relog_img[1] + 10)
    time.sleep(5)
    try:
        wechat_enter_img = pag.locateCenterOnScreen(
            os.path.join(os.getcwd(), "resources", "images", "wechat_login_enter.png"), confidence=0.8)
    except pag.ImageNotFoundException:
        return False
    pag.click(x=wechat_enter_img[0] + 10, y=wechat_enter_img[1] + 10)
