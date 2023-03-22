# coding=UTF-8
from tkinter import PhotoImage
import game
from os import path


# 牌類
class Tile:
    len = 84     # 牌的尺寸
    wid = 64     # 牌的尺寸
    d = path.dirname(__file__)
    q = path.dirname(d)
    p = path.dirname(q)

    def __init__(self, color, number):
        self.color = color         # 0為萬子，1為筒子，2為索子，3為風牌，4為三元牌
        self.number = number       # 0123分別為東南西北，012分別為白發中
        self.value = 10 * color + number     # 牌的大小（用以排序）

        self.image = []   # 儲存牌的圖案所包含的圖形的標識號
        # 自家手牌
        self.pic = PhotoImage(file=Tile.p + "/pai/pai/%d.gif" % self.value)

        # 各家河牌（包括上下家手牌）
        self.pic0 = PhotoImage(file=Tile.p + "/pai/0/%d.gif" % self.value)
        self.pic1 = PhotoImage(file=Tile.p + "/pai/1/%d.gif" % self.value)
        self.pic2 = PhotoImage(file=Tile.p + "/pai/2/%d.gif" % self.value)
        self.pic3 = PhotoImage(file=Tile.p + "/pai/3/%d.gif" % self.value)

        # 對家手牌
        self.pic4 = PhotoImage(file=Tile.p + "/pai/pai2/%d.gif" % self.value)

        self.isAbandoned = 0         # 是否是被打出的牌
        self.x = -1      # 牌在手牌中的位置

    # 畫手牌中的牌
    def draw(self, seat, canvas):
        # 自家
        if seat == 0:
            x = (1380 - 15 * Tile.wid) / 2 + self.x * Tile.wid
            y = 600
            p1, p2, p3 = (x, y), (x + Tile.wid, y), (x + Tile.wid, y + Tile.len)
            p4 = (x + Tile.wid * 1.25, y + Tile.len * 0.8)
            p5 = (x + Tile.wid * 1.25, y - Tile.len / 5)
            p6 = (x + Tile.wid / 4, y - Tile.len / 5)
            self.image += [canvas.create_polygon(p1, p2, p5, p6, outline="black", width=5, fill="white")]
            self.image += [canvas.create_polygon(p2, p3, p4, p5, outline="black", width=5, fill="white")]
            self.image += [canvas.create_image(x + 3, y + 3, anchor='nw', image=self.pic)]
            canvas.tag_bind(self.image[2], '<Button-1>', self.click)
            self.image += [canvas.create_rectangle(p1, p3, outline="black", width=5)]
        # 下家
        if seat == 1:
            x = 1380 - 80 - 45
            y = 690 - ((700 - 15 * 45) / 2 + (self.x + 1) * 45)
            p = (x + Tile.len / 4, y + 45)
            self.image += [canvas.create_rectangle(x, y, p, outline="black", width=5, fill="white")]
        # 對家
        if seat == 2:
            x = 1380 - ((1380 - 15 * Tile.wid) / 2 + (self.x + 1) * Tile.wid)
            y = 70
            p = (x + Tile.wid, y + Tile.len / 4)
            self.image += [canvas.create_rectangle(x, y, p, outline="black", width=5, fill="white")]
        # 上家
        if seat == 3:
            x = 80
            y = (700 - 17 * 45) / 2 + (self.x + 1) * 45
            p = (x + Tile.len / 4, y + 45)
            self.image += [canvas.create_rectangle(x, y, p, outline="black", width=5, fill="white")]

    # 畫河牌
    def draw_kawa(self, seat, p1, p2, canvas):
        self.clear(canvas)
        self.image += [canvas.create_rectangle(p1, p2, outline="black", width=5)]
        if seat == 0:
            self.image += [canvas.create_image(p1[0] + 3, p1[1] + 3, anchor='nw', image=self.pic0)]
        if seat == 1:
            self.image += [canvas.create_image(p1[0] + 3, p1[1] + 3, anchor='nw', image=self.pic1)]
        if seat == 2:
            self.image += [canvas.create_image(p1[0] + 3, p1[1] + 3, anchor='nw', image=self.pic2)]
        if seat == 3:
            self.image += [canvas.create_image(p1[0] + 3, p1[1] + 3, anchor='nw', image=self.pic3)]

    # 清除牌的圖畫
    def clear(self, canvas):
        if self.image:
            for j in self.image:
                canvas.delete(j)
        self.image = []

    # 打出這張牌
    def click(self, event):
        if game.Game.time_for == 4:
            self.isAbandoned = 1
            game.Game.time_for = 2
