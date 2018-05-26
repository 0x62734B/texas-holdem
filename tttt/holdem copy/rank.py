import random

def fresh_deck():
    suits = ("SPADE", "HEART", "DIAMOND", "CLUB")
    ranks = ("A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K")
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append([suit, rank])
    random.shuffle(deck)
    return deck

def str_to_int(card_list):  # 카드순위를 계산하기 쉽게 문양도 숫자로 변환
    for card in card_list:
        if card[0] == "SPADE":
            card[0] = 0
        elif card[0] == "HEART":
            card[0] = 1
        elif card[0] == "DIAMOND":
            card[0] = 2
        elif card[0] == "CLUB":
            card[0] = 3
        if card[1] == "A":  # ACE가 가장 높은 카드이므로 14로 배정
            card[1] = 14
        elif card[1] == "K":
            card[1] = 13
        elif card[1] == "Q":
            card[1] = 12
        elif card[1] == "J":
            card[1] = 11
        else:
            card[1] = int(card[1])
    return card_list

def int_to_str(card_list):
    for card in card_list:
        if card[0] == 0:
            card[0] = "Spade"
        elif card[0] == 1:
            card[0] = "Heart"
        elif card[0] == 2:
            card[0] = "Diamond"
        elif card[0] == 3:
            card[0] = "Club"
        if card[1] == 14:
            card[1] = "A"
        elif card[1] == 13:
            card[1] = "K"
        elif card[1] == 12:
            card[1] = "Q"
        elif card[1] == 11:
            card[1] = "J"
    return card_list

def get_rank(card_list):
    hand = sorted(card_list)
    rank_list = []
    for x in hand:
        rank_list.append(x[1])
    rank_list.sort()
    # 순위(순위가 같은 경우 추후에 계산)
    # 000 ~ 001 Royal Flush
    # 002 ~ 010 Straight Flush
    # 011 ~ 023 Four Card
    # 024 ~ 036 Full House
    # 037 ~ 044 Flush
    # 045 ~ 054 Straight
    # 055 ~ 067 Triple
    # 068 ~ 145 Two Pair
    # 146 ~ 158 One Pair
    # 159 ~ 166 High Card

    rank_name = "High_Card"
    rank = 173 - max(rank_list)

    Four_card = False
    Full_House = False

    Four_card_number = 0
    Triple_list = []
    Pair_list = []

    for x in range(15, 1, -1):
        if rank_list.count(x) == 4:    # 같은 숫자가 4개
            Four_card_number = x
        if rank_list.count(x) == 3:    # 같은 숫자가 3개 (2개 이상일 수 있으므로 리스트)
            Triple_list.append(x)
        if rank_list.count(x) == 2:    # 같은 숫자가 2개 (2개 이상일 수 있으므로 리스트)
            Pair_list.append(x)

    if Four_card_number > 0:
        Four_card = True
        rank = 25 - Four_card_number
        rank_name = "Four_Card"

    elif Triple_list != []:
        if Pair_list != []:             # Full House
            Full_House = True
            rank = 38 - Triple_list[0]
            rank_name = "Full_House"
        else:
            rank = 69 - Triple_list[0]
            rank_name = "Triple"

    elif Pair_list != []:
        if len(Pair_list) >= 2:
            rank_name = "Two_Pair"
            if Pair_list[0] == 14:
                rank = 81 - Pair_list[1]
            elif Pair_list[0] == 13:
                rank = 92 - Pair_list[1]
            elif Pair_list[0] == 12:
                rank = 102 - Pair_list[1]
            elif Pair_list[0] == 11:
                rank = 111 - Pair_list[1]
            elif Pair_list[0] == 10:
                rank = 119 - Pair_list[1]
            elif Pair_list[0] == 9:
                rank = 126 - Pair_list[1]
            elif Pair_list[0] == 8:
                rank = 132 - Pair_list[1]
            elif Pair_list[0] == 7:
                rank = 137 - Pair_list[1]
            elif Pair_list[0] == 6:
                rank = 141 - Pair_list[1]
            elif Pair_list[0] == 5:
                rank = 144 - Pair_list[1]
            elif Pair_list[0] == 4:
                rank = 146 - Pair_list[1]
            elif Pair_list[0] == 3:
                rank = 145
        elif len(Pair_list) == 1:
            if rank > 146:
                rank = 160 - Pair_list[0]
                rank_name = "One_Pair"
    Straight = False
    top_number = 0
    for i in range(len(rank_list)-4):
        if rank_list[i+1]-rank_list[i] == 1 and \
            rank_list[i+2]-rank_list[i+1] == 1 and \
            rank_list[i+3]-rank_list[i+2] == 1 and \
            rank_list[i+4]-rank_list[i+3] == 1:
            Straight = True
            top_number = rank_list[i+4]
    if Straight:
        if top_number == 14:
            rank = 45
            rank_name = "Mountain"
        else:
            rank = 59 - top_number
            rank_name = "Straight"
    if 2 in rank_list and 3 in rank_list and \
        4 in rank_list and 5 in rank_list and \
        14 in rank_list:                          # A 2 3 4 5 스트레이트는 숫자상으로 2 3 4 5 14 이므로 이렇게 표현
        rank = 54
        rank_name = "Straight"

    suit_list = []
    for x in hand:
        suit_list.append(x[0])

    if Four_card or Full_House:                # Flush보다 높은 족보
        pass
    else:
        Flush = False
        num = []
        if suit_list.count(0) >= 5:
            Flush = True
            pattern_num = 0
            for x in range(0, len(hand)):                     # 문양이 다른 카드는 삭제한다.
                if suit_list[len(hand)-1-x] != pattern_num:
                    del hand[len(hand)-1-x]
            for x in hand:
                num.append(x[1])
            rank = 51 - max(num)
            rank_name = "Spade_Flush"
        elif suit_list.count(1) >= 5:
            Flush = True
            pattern_num = 1
            for x in range(0, len(hand)):
                if suit_list[len(hand) - 1 - x] != pattern_num:
                    del hand[len(hand) - 1 - x]
            for x in hand:
                num.append(x[1])
            rank = 51 - max(num)
            rank_name = "Heart_Flush"
        elif suit_list.count(2) >= 5:
            Flush = True
            pattern_num = 2
            for x in range(0, len(hand)):
                if suit_list[len(hand) - 1 - x] != pattern_num:
                    del hand[len(hand) - 1 - x]
            for x in hand:
                num.append(x[1])
            rank = 51 - max(num)
            rank_name = "Diamond_Flush"
        elif suit_list.count(3) >= 5:
            Flush = True
            pattern_num = 3
            for x in range(0, len(hand)):
                if suit_list[len(hand) - 1 - x] != pattern_num:
                    del hand[len(hand) - 1 - x]
            for x in hand:
                num.append(x[1])
            rank = 51 - max(num)
            rank_name = "Club_Flush"
        if Flush:
            num.sort()
            if num[1]-num[0] == 1 and \
                num[2]-num[1] == 1 and \
                num[3]-num[2] == 1 and \
                num[4]-num[3] == 1:
                if max(num) == 14:
                    rank = 1
                    rank_name = "Royal_Flush"
                else:
                    rank = 15 - max(num)
                    rank_name = "Straight_Flush"
            if num == [2, 3, 4, 5, 14]:
                rank = 10
                rank_name = "Straight_Flush"

    return (rank, rank_name)