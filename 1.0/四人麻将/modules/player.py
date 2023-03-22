# coding=UTF-8
from tile import *


class Player:
    def __init__(self, seat):
        self.direction = 0   # 0123分別為東南西北家
        self.seat = seat     # 0123分別為自家（我），下家，對家，上家
        self.inHand = []     # 手牌
        self.inHandNum = 0   # 手牌張數
        self.furuNum = 0     # 副露組數
        self.furu = []       # 副露牌
        self.kawa = []       # 打出的河牌
        self.kawaNum = 0     # 河牌數
        self.next_player = None    # 下家

    # 理牌
    def sort(self):
        for i in range(self.inHandNum):
            for j in range((i + 1), self.inHandNum):
                if self.inHand[i].value > self.inHand[j].value:
                    self.inHand[i], self.inHand[j] = self.inHand[j], self.inHand[i]

    # 把摸來的牌插進手牌
    def insert(self):
        for i in range(self.inHandNum):
            if self.inHand[i].value > self.inHand[self.inHandNum - 1].value:
                for j in range(self.inHandNum - 2, i - 1, -1):
                    self.inHand[j], self.inHand[j + 1] = self.inHand[j + 1], self.inHand[j]
                break

    # 定位牌在手牌中的位置
    def find_position(self):
        for i in range(self.inHandNum):
            self.inHand[i].x = i

    # 畫手牌
    def draw(self, canvas):
        self.find_position()
        for i in range(self.inHandNum):
            self.inHand[i].draw(self.seat, canvas)

    # 畫河牌
    def draw_kawa(self, canvas):
        wid = 45
        # 自家
        if self.seat == 0:
            num = 15
            x = 315 + (self.kawaNum - 1) % num * wid + 30
            y = 440 + (self.kawaNum - 1) / num * wid * 4 / 3
            p1 = (x, y)
            p2 = (x + wid, y + wid * 4 / 3)
            self.kawa[self.kawaNum - 1].draw_kawa(self.seat, p1, p2, canvas)
        # 下家
        if self.seat == 1:
            num = 10
            y = (700 - num * wid) / 2 - (self.kawaNum - 1) % num * wid + num * wid - 60
            x = 1052 + (self.kawaNum - 1) / num * wid * 4 / 3
            p1 = (x, y)
            p2 = (x + wid * 4 / 3, y + wid)
            self.kawa[self.kawaNum - 1].draw_kawa(self.seat, p1, p2, canvas)
        # 對家
        if self.seat == 2:
            num = 15
            x = 945 - (self.kawaNum - 1) % num * wid + 30
            y = 170 - (self.kawaNum - 1) / num * wid * 4 / 3
            p1 = (x, y)
            p2 = (x + wid, y + wid * 4 / 3)
            self.kawa[self.kawaNum - 1].draw_kawa(self.seat, p1, p2, canvas)
        # 上家
        if self.seat == 3:
            num = 10
            y = (700 - num * wid) / 2 + (self.kawaNum - 1) % num * wid - 15
            x = 250 - (self.kawaNum - 1) / num * wid * 4 / 3
            p1 = (x, y)
            p2 = (x + wid * 4 / 3, y + wid)
            self.kawa[self.kawaNum - 1].draw_kawa(self.seat, p1, p2, canvas)

    # 清除牌圖畫
    def clear(self, canvas):
        for i in self.inHand:
            i.clear(canvas)
