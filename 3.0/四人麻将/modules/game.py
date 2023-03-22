# coding=UTF-8
from player import *
from yama import *
from time import *
from thread import *


class Game:
    isInTurn = Player(0)    # 當前出牌玩家
    hoochan = Player(0)     # 放銃者
    isOver = 0              # 遊戲是否結束
    nowGet = None           # 目前摸到的牌
    nowThrow = None         # 目前打出的牌
    time_for = -1
    # 0為摸牌時間，1為電腦玩家思考時間，2為出牌時間，3為判定時間，4為自家思考出牌時間，5為自家決策吃 碰 明槓 食胡時間，6為自家決策暗槓 加槓 自摸，-1為其他時間

    def __init__(self, c):
        self.canvas = c       # 畫布

        self.yama = Yama()    # 牌山

        # 生成玩家
        self.players = []     # 儲存玩家的列表
        for i in range(4):
            self.players += [Player(i)]  # 0123分別為自家（我），下家，對家，上家
        for i in range(4):
            self.players[i].next_player = self.players[(i + 1) % 4]
            self.players[i].last_palyer = self.players[(i + 3) % 4]

        self.buttons = [0] * 5

    # 起牌時理牌動畫效果線程
    def first_sort_thread(self):
        sleep(0.5)
        self.players[0].sort()
        self.players[0].draw(self.canvas)
        sleep(0.5)

        # 給予莊家牌權
        for i in self.players:
            if i.direction == 0:
                Game.isInTurn = i
                break
        Game.time_for = 0

    # 起牌
    def start_game(self):
        # 找東家
        a = 0
        for a in range(4):
            if self.players[a].direction == 0:
                break
        # 配牌
        for i in range(3):
            for j in range(4):
                self.players[(a + j) % 4].inHand += self.yama.tiles[Yama.first:(Yama.first + 4)]
                Yama.first += 4
                Yama.TOTAL -= 4
        for j in range(4):
            self.players[(a + j) % 4].inHand += [self.yama.tiles[Yama.first]]
            self.players[(a + j) % 4].inHandNum = 13
            Yama.first += 1
            Yama.TOTAL -= 1

        # 理牌
        self.players[0].draw(self.canvas)
        for i in [1, 2, 3]:
            self.players[i].sort()
            self.players[i].draw(self.canvas)
        start_new_thread(self.first_sort_thread, ())

    # 摸牌
    def get_tile(self, x):    # x = 0為從牌山首摸牌，x = 1為從牌山末摸牌
        if x == 0:
            Game.nowGet = self.yama.tiles[Yama.first]
            Yama.first += 1
        else:
            Game.nowGet = self.yama.tiles[Yama.last]
            Yama.last -= 1
            Yama.first += 1
        Yama.TOTAL -= 1
        Game.isInTurn.inHand += [Game.nowGet]
        Game.isInTurn.inHandNum += 1
        Game.nowGet.x = Game.isInTurn.inHandNum
        if Game.isInTurn.seat != 2 and Game.isInTurn.seat != 0:
            Game.nowGet.x -= 0.5
        Game.nowGet.draw(Game.isInTurn.seat, self.canvas)
        Game.isInTurn.insert()
        if Game.isInTurn.seat:
            Game.time_for = 1
        else:
            Game.time_for = 4

        # l = [2,3,4,4,5,5,6,0,0,0,0,0,0,0]
        # s = set()
        # for i in range(self.players[0].inHandNum):
        #     self.players[0].inHand[i].value = l[i]    # 測試代碼
        # self.yama.tiles[self.yama.first].value = 4
        # for i in self.yama.tiles:
        #     if self.players[0].can_ron(i.value):
        #         s.add(i.value)
        # print s

        self.judge2()

    # 思考計算
    def thinking(self):
        # 這裡需要修改
        sleep(1)
        Game.nowGet.isAbandoned = 1
        Game.time_for = 2

    # 出牌
    def throw_tile(self):
        for i in range(Game.isInTurn.inHandNum):
            if Game.isInTurn.inHand[i].isAbandoned:
                Game.nowThrow = Game.isInTurn.inHand[i]
                Game.isInTurn.kawa += [Game.nowThrow]
                Game.isInTurn.kawaNum += 1
                del Game.isInTurn.inHand[i]
                Game.isInTurn.inHandNum -= 1
                break
        Game.nowThrow.clear(self.canvas)
        sleep(0.5)
        Game.nowGet.clear(self.canvas)
        Game.isInTurn.draw_kawa(self.canvas)
        self.canvas.itemconfig(Game.isInTurn.kawa[Game.isInTurn.kawaNum - 1].image[0], outline="red")
        Game.isInTurn.draw(self.canvas)
        Game.time_for = 3

    # 自家吃牌
    # 自家碰牌
    def pon(self, event):
        self.players[0].pon(self.canvas)
        Game.isInTurn.kawa[Game.isInTurn.kawaNum - 1].clear(self.canvas)
        del Game.isInTurn.kawa[Game.isInTurn.kawaNum - 1]
        Game.isInTurn.kawaNum -= 1
        Game.isInTurn = self.players[0]
        Game.isInTurn.draw(self.canvas)
        for i in self.buttons:
            if i:
                self.canvas.delete(i)
        self.buttons = [0] * 5
        Game.time_for = 4

    # 自家明槓
    def kann(self, event):
        self.players[0].kann(self.canvas)
        Game.isInTurn.kawa[Game.isInTurn.kawaNum - 1].clear(self.canvas)
        del Game.isInTurn.kawa[Game.isInTurn.kawaNum - 1]
        Game.isInTurn.kawaNum -= 1
        Game.isInTurn = self.players[0]
        Game.isInTurn.draw(self.canvas)
        for i in self.buttons:
            if i:
                self.canvas.delete(i)
        self.buttons = [0] * 5
        self.get_tile(1)

    # 自家暗槓
    # 自家加槓

    # 自家食和
    def ron(self, event):
        Game.hoochan = Game.isInTurn
        for i in self.buttons:
            if i:
                self.canvas.delete(i)
        self.buttons = [0] * 5
        self.canvas.create_text(690, 350, text="点了", fill='red', font=('楷体', 100, 'bold'))
        Game.isOver = 1

    # 自家自摸

    # 自家取消活動機會
    def cancel(self, event):
        for i in self.buttons:
            if i:
                self.canvas.delete(i)
        self.buttons = [0] * 5
        self.canvas.itemconfig(Game.isInTurn.kawa[Game.isInTurn.kawaNum - 1].image[0], outline="black")
        Game.isInTurn = Game.isInTurn.next_player
        Game.time_for = 0

    # 判定吃 碰 明槓 食和
    def judge(self):
        sleep(0.5)
        f = 0
        if self.players[0].can_pon(Game.nowThrow.value):
            f = 1
            self.buttons[1] = self.canvas.create_text(600, 350, text="碰", fill='red', font=('楷体', 50, 'bold'))
            self.canvas.tag_bind(self.buttons[1], '<Button-1>', self.pon)
        if Game.isInTurn.seat != 0 and self.players[0].can_kann(Game.nowThrow.value):
            f = 1
            self.buttons[2] = self.canvas.create_text(690, 350, text="杠", fill='red', font=('楷体', 50, 'bold'))
            self.canvas.tag_bind(self.buttons[2], '<Button-1>', self.kann)
        if Game.isInTurn.seat != 0 and self.players[0].can_ron(Game.nowThrow.value):
            f = 1
            self.buttons[3] = self.canvas.create_text(780, 350, text="和", fill='red', font=('楷体', 50, 'bold'))
            self.canvas.tag_bind(self.buttons[3], '<Button-1>', self.ron)
        if f:
            Game.time_for = 5
            self.buttons[4] = self.canvas.create_text(500, 350, text="×", fill='red', font=('楷体', 50, 'bold'))
            self.canvas.tag_bind(self.buttons[4], '<Button-1>', self.cancel)
        else:
            self.canvas.itemconfig(Game.isInTurn.kawa[Game.isInTurn.kawaNum - 1].image[0], outline="black")
            Game.isInTurn = Game.isInTurn.next_player
            Game.time_for = 0

    # 判定暗槓 加槓 自摸
    def judge2(self):
        if Game.isInTurn.is_tsumo():
            self.canvas.create_text(690, 350, text="摸了", fill='red', font=('楷体', 100, 'bold'))
            Game.isOver = 1

    # 遊戲進行線程
    def game_thread(self):
        while not Game.isOver:
            if Game.time_for == 0:
                self.get_tile(0)
            if Game.time_for == 1:
                self.thinking()
            if Game.time_for == 2:
                self.throw_tile()
            if Game.time_for == 3:
                self.judge()

    # 遊戲進行中
    def in_game(self):
        start_new_thread(self.game_thread, ())
