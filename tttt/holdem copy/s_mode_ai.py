from tttt.holdem.class_card import *
from tttt.holdem.class_ai import *
from tttt.holdem.class_player import *


import random
import pygame
import tttt.holdem.constants as c
import tttt.holdem.rank as r

player1 = []
player2 = []
community = []
deck = []
small_blind = 1
max_player = 2
me = player(1,275)
com = ai(2,250)
divided = False
race_step = 0
bet_state = 50
my_bet = 25
com_bet = 50
def fresh_deck(mode):
    global deck, first, player1, player2, community
    new = []
    suits = ["SPADE", "HEART", "DIAMOND", "CLUB"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    for i in range(len(suits)):
        for j in range(len(ranks)):
            new.append([suits[i], ranks[j]])
    random.shuffle(new)

    # 플레이어에게 배분
    for i in range(2):
        for j in range(max_player):
            give = (small_blind + (i*2 + j)) % max_player
            if give == 0:
                give = max_player
            deck.append(card(new[i*2 + j], give, i + 1, mode))
            if (j+1) % max_player == 1:
                player1.append(new[i*2+j])
            elif (j+1) % max_player == 0:
                player2.append(new[i*2 +j])

    # 커뮤니티 카드
    for i in range(max_player*2 + 1, max_player*2 + 6):
        deck.append(card(new[i], "COMMUNITY", i - (max_player * 2), mode))
        community.append(new[i])

def div_animation():
    i = 0
    while True:
        if deck[i].get_moved:
            deck[i].show()
        else:
            for j in range(i + 1, max_player * 2 + 5):
                deck[j].show()
            deck[i].show(True)
            break
        i += 1
        if i >= max_player * 2 + 5:
            global divided
            divided = True
            break


def GAME_AI_SCREEN(mode):
    global deck, divided, player1, player2, community, race_step
    if mode == "EASY":
        c.SCREEN.blit(c.AI_EASY_BACK, (0,0))
    elif mode == "NORMAL":
        pass
    elif mode == "HARD":
        pass

    if not deck: # 덱이 비었을때
        fresh_deck(mode)

    if not divided:
        div_animation()
    else:
        opened = False
        check = 0
        for i in range(max_player*2 + 5):
            if deck[i].get_owner == 1 and not deck[i].get_faced:
                deck[i].show(False, True)
            elif race_step and max_player*2 <= i < (max_player*2 + 5) - (3-race_step):
                deck[i].show(False, True)
            else:
                deck[i].show()
            if deck[i].get_faced:
                check += 1

        if check == 2 + (3 if race_step == 1 else (0 if race_step == 0 else 2 + race_step)):
            opened = True

        if opened:
            command = input("콜/레이즈/폴드 : ")
            if command == "콜":
                me.bet(bet_state - my_bet)
                com.bet(bet_state - com_bet)
                race_step += 1

        if race_step == 4:
            deck[1].show(False, True)
            deck[3].show(False, True)

        if check == 9:
            check += 11
            player1_int = r.str_to_int(player1+community)
            player2_int = r.str_to_int(player2+community)
            player1_num = [player1_int[0][1], player1_int[1][1]]
            player2_num = [player2_int[0][1], player2_int[1][1]]
            player1_rank = r.get_rank(player1_int)
            player2_rank = r.get_rank(player2_int)
            if player1_rank[0] > player2_rank[0]:
                print("Your rank is ",player1_rank[1],"\nAI's rank is ",player2_rank[1],"\nYou lose")
            elif player1_rank[0] < player2_rank[0]:
                print("Your rank is ",player1_rank[1],"\nAI's rank is ",player2_rank[1],"\nYou won")
            elif player1_rank[0] == player2_rank[0]:
                if max(player1_num) > max(player2_num):
                    print("You won")
                elif max(player1_num) < max(player2_num):
                    print("You lose")
                elif max(player):
                    pass