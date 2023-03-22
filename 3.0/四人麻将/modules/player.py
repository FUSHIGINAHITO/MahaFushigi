# coding=UTF-8
from tile import *
import game


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
        self.last_player = None    # 上家

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
        self.clear(canvas)
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

    # 清除手牌圖畫
    def clear(self, canvas):
        for i in self.inHand:
            if i:
                i.clear(canvas)

    # 判斷进某张后能否和牌
    def is_hu(self, value):
        yaojiu = [1, 9, 11, 19, 21, 29, 30, 31, 32, 33, 40, 41, 42]   # 幺九牌
        hand = []       # 手牌
        tmp = []
        duizi = set()   # 對子
        for i in range(self.inHandNum):
            hand += [self.inHand[i].value]
            tmp += [0]
        if value:
            hand += [value]
            tmp += [0]
        length = len(hand)
        # 手牌排序
        for i in range(length):
            for j in range(i + 1, length):
                if hand[i] > hand[j]:
                    hand[i], hand[j] = hand[j], hand[i]
        # 找成對的
        for i in range(length):
            for j in range(i + 1, length):
                if hand[i] == hand[j]:
                    duizi.add(hand[j])
        # 判斷七對子
        if len(duizi) == 7:
            return 1
        # 判斷十三幺
        flag = 1
        for i in hand:
            if i not in yaojiu:
                flag = 0
                break
        if flag and len(duizi) == 1 and length == 14:
            return 1
        # 判斷普通和牌
        for i in duizi:
            flag = 1
            k = 0
            for j in range(length):
                if hand[j] == i:
                    tmp[j] = i
                    hand[j] = 0
                    k += 1
                if k == 2:
                    break
            for j in range(length - 2):
                if hand[j] != 0:
                    f = 1
                    tmp[j] = hand[j]
                    hand[j] = 0
                    if hand[j + 1] == tmp[j] and hand[j + 2] == tmp[j]:
                        tmp[j + 1], tmp[j + 2] = hand[j + 1], hand[j + 2]
                        hand[j + 1], hand[j + 2] = 0, 0
                        f = 0
                    elif tmp[j] <= 27 and tmp[j] + 1 in hand and tmp[j] + 2 in hand:
                        for n in range(2):
                            for k in range(j + 1, length):
                                if hand[k] == tmp[j] + 1 + n:
                                    tmp[k] = tmp[j] + 1 + n
                                    hand[k] = 0
                                    break
                        f = 0
                    if f:
                        break
            for j in hand:
                if j:
                    flag = 0
            if flag:
                return 1
            else:
                for j in range(length):
                    if hand[j] == 0:
                        hand[j] = tmp[j]
                        tmp[j] = 0
        return 0

    # 判斷吃牌
    def can_chi(self):
        return 0

    # 判斷碰牌
    def can_pon(self, value):
        if game.Game.isInTurn.seat != self.seat:
            k = 0
            for i in range(self.inHandNum):
                if self.inHand[i].value == value:
                    k += 1
            if k > 1:
                return 1
        return 0

    def pon(self, canvas):
        self.furuNum += 1
        self.furu += [game.Game.nowThrow]
        for j in range(2):
            for i in range(self.inHandNum):
                if self.inHand[i].value == game.Game.nowThrow.value:
                    self.furu += [self.inHand[i]]
                    self.inHand[i].clear(canvas)
                    del self.inHand[i]
                    self.inHandNum -= 1
                    break

    # 判斷明槓
    def can_kann(self, value):
        k = 0
        for i in range(self.inHandNum):
            if self.inHand[i].value == value:
                k += 1
        if k == 3:
            return 1
        else:
            return 0

    def kann(self, canvas):
        self.furuNum += 1
        self.furu += [game.Game.nowThrow]
        for j in range(3):
            for i in range(self.inHandNum):
                if self.inHand[i].value == game.Game.nowThrow.value:
                    self.furu += [self.inHand[i]]
                    self.inHand[i].clear(canvas)
                    del self.inHand[i]
                    self.inHandNum -= 1
                    break

    # 判斷食和
    def can_ron(self, value):
        if self.is_hu(value):
            return 1
        else:
            return 0

    # 判斷暗槓
    def can_ankann(self):
        return 0

    # 判斷自摸
    def is_tsumo(self):
        if self.is_hu(0):
            return 1
        else:
            return 0
