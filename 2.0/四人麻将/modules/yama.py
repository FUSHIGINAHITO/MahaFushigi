# coding=UTF-8
from tile import *
from random import *


# 牌山類
class Yama:
    TOTAL = 136       # 牌山剩餘張數
    first = 0         # 牌山首張
    last = TOTAL - 1  # 牌山末張

    def __init__(self):
        self.tiles = []       # 牌山

        # 生成數牌
        for i in range(3):
            for j in range(1, 10):
                for k in range(4):
                    self.tiles += [Tile(i, j)]
        # 生成風牌
        for i in range(4):
            for j in range(4):
                self.tiles += [Tile(3, i)]
        # 生成三元牌
        for i in range(3):
            for j in range(4):
                self.tiles += [Tile(4, i)]
        self.xipai()

    # 洗牌
    def xipai(self):
        shuffle(self.tiles)
