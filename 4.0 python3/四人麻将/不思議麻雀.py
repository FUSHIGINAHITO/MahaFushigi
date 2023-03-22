# coding=UTF-8
from tkinter import *
from os import path
import sys
d = path.dirname(__file__)
p = path.dirname(d)
sys.path.append(d + '/modules/')
from game import *


def new_game():
    game.yama.xipai()
    return


def root_menu():
    main_menu = Menu(root)
    start_menu = Menu(main_menu)
    main_menu.add_cascade(label="開始", menu=start_menu)
    start_menu.add_command(label='新遊戲', command=new_game)
    start_menu.add_command(label='***', command=new_game)
    start_menu.add_separator()
    start_menu.add_command(label='設置', command=new_game)
    start_menu.add_separator()
    start_menu.add_command(label='退出', command=root.quit)
    help_menu = Menu(main_menu)
    main_menu.add_cascade(label="幫助", menu=help_menu)
    help_menu.add_command(label='操作指南', command=new_game)
    help_menu.add_command(label='作弊', command=new_game)
    root.config(menu=main_menu)


root = Tk()
root.title('不思議麻雀')
root.geometry('1380x700')
root_menu()

ID = p + "/background/"
canvas = Canvas(root, height=700, width=1380, bg='black')
canvas.place(x=-1, y=-4)
pic = PhotoImage(file="%s3.gif" % ID)
canvas.create_image(0, 0, anchor=NW, image=pic)

# 開局
game = Game(canvas)
# 起牌
game.start_game()
game.in_game()

root.mainloop()
