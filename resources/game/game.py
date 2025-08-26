# game.py
import os, json, winsound, multiprocessing


# 2. 长度计算（中文算 2）
def wlen(s):
    return sum(2 if 0x4E00 <= ord(ch) <= 0x9FFF else 1 for ch in s)


TOTAL = 130  # 总显示宽度
BAR = '#' * (TOTAL + 2)


def center(txt):
    pad = TOTAL - wlen(txt)
    left = pad // 2
    return ' ' * left + txt + ' ' * (TOTAL - left - wlen(txt))


def format_text(text, kind):
    match kind:
        case None:
            return text
        case "red":
            return f"\033[31m{text}\033[0m"
        case "green":
            return f"\033[32m{text}\033[0m"
        case "yellow":
            return f"\033[33m{text}\033[0m"
        case "blue":
            return f"\033[34m{text}\033[0m"
        case "magenta":
            return f"\033[35m{text}\033[0m"
        case "cyan":
            return f"\033[36m{text}\033[0m"
        case "bold":
            return f"\033[1m{text}\033[0m"
        case _:
            return text

def show_text(file_path):
    text = json.load(open(file_path, encoding='utf-8'))
    title = text["info"]["title"]
    date = text["info"]["date"]
    recorder = text["info"]["author"]
    data_list = text["data"]
    for data in data_list:
        if data.get("sound", None):
            if os.path.splitext(data.get("sound", None))[1] == ".wav_l":
                winsound.PlaySound(data.get("sound", None).replace(".wav_l", ".wav"), winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
            else:
                winsound.PlaySound(data.get("sound", None), winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            winsound.PlaySound(None, winsound.SND_PURGE)
        os.system('cls')
        os.system('title ' + title)
        print(BAR)
        print('#' + center('') + '#')
        print('#' + center(title) + '#')
        print('#' + center('') + '#')
        print(BAR)
        print('#' + center('') + '#')
        print('#' + center(f'date:{date}') + '#')
        print('#' + center(f'recorder:{recorder}') + '#')
        print('#' + center('') + '#')
        print(BAR)
        print('#' + center('') + '#')
        text_data = '#' + center(data.get("text")) + '#'
        color = data.get("color", None)
        print(format_text(text_data, color))
        print('#' + center('') + '#')
        print(BAR)
        input("[请按回车键继续]")
        if data.get("command", None):
            os.system(data.get("command"))

if __name__ == '__main__':
    show_text("1.json")
    show_text("coming soon.json")
