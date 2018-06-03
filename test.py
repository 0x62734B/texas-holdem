def get_potential_rank(card_list):
    hand = sorted(card_list)
    rank_list = []
    for x in hand:
        rank_list.append(x[1])
    rank_list.sort()  # 숫자만을 오름차순으로 정렬
    # 순위
    # Royal Flush >>> xxx
    # Straight Flush >>> xxx
    # four_card >> xxx
    # Full_House >> ooo
    # Flush  >> ooo
    # Straight  >> ooo
    # Triple  >> xxx >> potential_Four_Card,Full_House
    # Two_Pair >> xxx >> potential_Full_House
    # One_Pair >> xxx

    rank_name = "High_Card"

    if (2 in rank_list and 3 in rank_list and 4 in rank_list and 5 in rank_list) or \
            (3 in rank_list and 4 in rank_list and 5 in rank_list and 6 in rank_list) or \
            (4 in rank_list and 5 in rank_list and 6 in rank_list and 7 in rank_list) or \
            (5 in rank_list and 6 in rank_list and 7 in rank_list and 8 in rank_list) or \
            (6 in rank_list and 7 in rank_list and 8 in rank_list and 9 in rank_list) or \
            (7 in rank_list and 8 in rank_list and 9 in rank_list and 10 in rank_list) or \
            (8 in rank_list and 9 in rank_list and 10 in rank_list and 11 in rank_list) or \
            (9 in rank_list and 10 in rank_list and 11 in rank_list and 12 in rank_list) or \
            (10 in rank_list and 11 in rank_list and 12 in rank_list and 13 in rank_list) or \
            (11 in rank_list and 12 in rank_list and 14 in rank_list and 14 in rank_list) or \
            (14 in rank_list and 2 in rank_list and 3 in rank_list and 4 in rank_list) or \
            (2 in rank_list and 4 in rank_list and 5 in rank_list and 6 in rank_list) or \
            (3 in rank_list and 5 in rank_list and 6 in rank_list and 7 in rank_list) or \
            (4 in rank_list and 6 in rank_list and 7 in rank_list and 8 in rank_list) or \
            (5 in rank_list and 7 in rank_list and 8 in rank_list and 9 in rank_list) or \
            (6 in rank_list and 8 in rank_list and 9 in rank_list and 10 in rank_list) or \
            (7 in rank_list and 9 in rank_list and 10 in rank_list and 11 in rank_list) or \
            (8 in rank_list and 10 in rank_list and 11 in rank_list and 12 in rank_list) or \
            (9 in rank_list and 11 in rank_list and 12 in rank_list and 13 in rank_list) or \
            (10 in rank_list and 12 in rank_list and 13 in rank_list and 14 in rank_list) or \
            (14 in rank_list and 3 in rank_list and 4 in rank_list and 5 in rank_list) or \
            (2 in rank_list and 3 in rank_list and 5 in rank_list and 6 in rank_list) or \
            (3 in rank_list and 4 in rank_list and 6 in rank_list and 7 in rank_list) or \
            (4 in rank_list and 5 in rank_list and 7 in rank_list and 8 in rank_list) or \
            (5 in rank_list and 6 in rank_list and 8 in rank_list and 9 in rank_list) or \
            (6 in rank_list and 7 in rank_list and 9 in rank_list and 10 in rank_list) or \
            (7 in rank_list and 8 in rank_list and 10 in rank_list and 11 in rank_list) or \
            (8 in rank_list and 9 in rank_list and 11 in rank_list and 12 in rank_list) or \
            (9 in rank_list and 10 in rank_list and 12 in rank_list and 13 in rank_list) or \
            (10 in rank_list and 11 in rank_list and 13 in rank_list and 14 in rank_list) or \
            (14 in rank_list and 2 in rank_list and 4 in rank_list and 5 in rank_list) or \
            (2 in rank_list and 3 in rank_list and 4 in rank_list and 6 in rank_list) or \
            (3 in rank_list and 4 in rank_list and 5 in rank_list and 7 in rank_list) or \
            (4 in rank_list and 5 in rank_list and 6 in rank_list and 8 in rank_list) or \
            (5 in rank_list and 6 in rank_list and 7 in rank_list and 9 in rank_list) or \
            (6 in rank_list and 7 in rank_list and 8 in rank_list and 10 in rank_list) or \
            (7 in rank_list and 8 in rank_list and 9 in rank_list and 11 in rank_list) or \
            (8 in rank_list and 9 in rank_list and 10 in rank_list and 12 in rank_list) or \
            (9 in rank_list and 10 in rank_list and 11 in rank_list and 13 in rank_list) or \
            (10 in rank_list and 11 in rank_list and 12 in rank_list and 14 in rank_list) or \
            (14 in rank_list and 2 in rank_list and 3 in rank_list and 5 in rank_list):
        rank_name = "P_Straight"

        suit_list = []
        for x in hand:
            suit_list.append(x[0])
        for i in range(4):
            if suit_list.count(i) == 4:
                rank_name = "P_Flush"

    return rank_name