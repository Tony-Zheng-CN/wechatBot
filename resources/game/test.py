#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random, sys, time, os

SAVE = ".undertale_cli_save"
import msvcrt


class _Getch:
    def __call__(self):
        return msvcrt.getch().decode('utf-8')


getch = _Getch()

# ---------- 工具 ----------
cls = lambda: os.system("cls" if os.name=="nt" else "clear")
def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

# ---------- 战斗 ----------
class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x, self.y, self.dx, self.dy = x, y, dx, dy
    def step(self, w, h):
        self.x += self.dx
        self.y += self.dy
        return 0 <= self.x < w and 0 <= self.y < h

class BulletBoard:
    def __init__(self, w=20, h=10):
        self.w, self.h = w, h
        self.bullets = []
        self.player = (w//2, h-1)
    def spawn_circle(self, n=8):
        cx, cy = self.w//2, 3
        for i in range(n):
            ang = 2*3.1416*i/n
            dx, dy = int(2*round(2*random.random()*ang)), int(2*round(2*random.random()*ang))
            self.bullets.append(Bullet(cx, cy, dx, dy))
    def step(self):
        self.bullets = [b for b in self.bullets if b.step(self.w, self.h)]
    def hit(self):
        px, py = self.player
        return any(abs(b.x-px)<1 and abs(b.y-py)<1 for b in self.bullets)
    def draw(self):
        grid = [[" "]*self.w for _ in range(self.h)]
        for b in self.bullets:
            if 0 <= b.x < self.w and 0 <= b.y < self.h:
                grid[b.y][b.x] = "*"
        px, py = self.player
        grid[py][px] = "♥"
        print("┌" + "─"*self.w + "┐")
        for row in grid:
            print("│" + "".join(row) + "│")
        print("└" + "─"*self.w + "┘")

class Enemy:
    def __init__(self, name, hp, atk):
        self.name, self.max_hp, self.hp, self.atk = name, hp, hp, atk
        self.mood = 0          # -2~2，越高越友善
    def color(self):
        if self.mood <= -1: return "\033[31m"      # 红
        if self.mood == 0:  return "\033[33m"      # 黄
        return "\033[32m"                          # 绿
    def mercy_available(self): return self.mood >= 2

class Player:
    def __init__(self, hp=20):
        self.max_hp, self.hp = hp, hp

def battle(player, enemy):
    board = BulletBoard()
    while True:
        cls()
        print(f"{enemy.color()}{enemy.name}\033[0m  HP {enemy.hp}/{enemy.max_hp}  Mood {enemy.mood}/2")
        print(f"♥ 你 HP {player.hp}/{player.max_hp}")
        print("1 Fight  2 Act  3 Item  4 Mercy")
        choice = input("> ").strip()
        if choice == "1":
            dmg = random.randint(3, 6)
            enemy.hp = max(enemy.hp - dmg, 0)
            print(f"你造成了 {dmg} 点伤害！")
            if enemy.hp == 0:
                slow_print("敌人被击败。"); return True
        elif choice == "2":
            print("你试图交谈... 情绪+1")
            enemy.mood = min(enemy.mood+1, 2)
        elif choice == "3":
            slow_print("你吃了肉桂兔包。HP+5")
            player.hp = min(player.hp+5, player.max_hp)
        elif choice == "4":
            if enemy.mercy_available():
                slow_print("你宽恕了敌人。"); return True
            else:
                slow_print("现在还不是宽恕的时候。")
        else:
            continue

        # Enemy turn + bullet hell
        slow_print(f"{enemy.name} 发起了弹幕攻击！WASD 移动，坚持 5 秒...")
        board.bullets.clear(); board.spawn_circle()
        end_time = time.time() + 5
        while time.time() < end_time:
            if getch() in {"w","W"}: board.player = (board.player[0], max(board.player[1]-1, 0))
            if getch() in {"s","S"}: board.player = (board.player[0], min(board.player[1]+1, board.h-1))
            if getch() in {"a","A"}: board.player = (max(board.player[0]-1, 0), board.player[1])
            if getch() in {"d","D"}: board.player = (min(board.player[0]+1, board.w-1), board.player[1])
            board.step()
            cls(); board.draw()
            if board.hit():
                dmg = random.randint(2, 5)
                player.hp -= dmg
                slow_print(f"被击中！HP -{dmg}")
                break
        else:
            slow_print("完美闪避！")
        if player.hp <= 0:
            slow_print("你倒下了...")
            return False

# ---------- 存档 ----------
def load_death_count():
    try:
        with open(SAVE) as f:
            return int(f.read())
    except:
        return 0
def save_death_count(n):
    with open(SAVE, "w") as f:
        f.write(str(n))

# ---------- 主流程 ----------
def main():
    death = load_death_count()
    if death:
        slow_print(f"你在这个世界已经死去 {death} 次...\n")
    player = Player()
    slow_print("欢迎来到「终端传说」（Terminal-tale）")
    slow_print("一朵会说话的小花出现在眼前：「在这个世界，不是杀人就是被杀！」")
    dummy = Enemy("训练假人", 10, 3)
    if battle(player, dummy):
        slow_print("小花：「什么？你居然... 算了，继续前进吧。」")
    else:
        slow_print("小花：「早就告诉过你了。」")
        save_death_count(death+1)
        sys.exit()
    slow_print("Demo 结束，感谢游玩！")

if __name__ == "__main__":
    main()