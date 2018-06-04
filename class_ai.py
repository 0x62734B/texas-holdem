import s_mode_ai as s
import random


class ai:
    def __init__(self, name, chips, mode):
        self.__name = name
        self.__chips = chips
        self.__mode = mode

        #default
        self.__cards = []
        self.__opened = False
        self.__betted = 0
        self.__folded = False
        self.__thinking = False
        self.__thinked = False
        self.__rank = ()

    @property
    def get_name(self):
        return self.__name

    @property
    def get_chips(self):
        return self.__chips

    def give_chips(self, chips):
        self.__chips += chips

    @property
    def get_opened(self):
        return self.__opened

    @property
    def get_betted(self):
        return self.__betted

    @property
    def get_folded(self):
        return self.__folded

    @property
    def reset_folded(self):
        self.__folded = False

    @property
    def get_thinked(self):
        return self.__thinked

    def set_chips(self, chips):
        self.__chips = chips

    @property
    def reset_betted(self):
        self.__betted = 0

    @property
    def reset_think(self):
        self.__thinking = False
        self.__thinked = False

    def get_card(self, index):
        return self.__cards[index]

    def give_card(self, card):
        self.__cards.append(card)

    @property
    def card_reset(self):
        self.__opened = False
        self.__cards = []
        self.__rank = ()

    @property
    def card_open(self):
        if not self.__opened:
            self.__cards[0].show(False, True)
            self.__cards[1].show(False, True)
        if self.__cards[0].get_faced and self.__cards[1].get_faced:
            self.__opened = True

    @property
    def card_show(self):
        self.__cards[0].show()
        self.__cards[1].show()

    def bet(self, chips):
        if chips == -1:
            self.__folded = True
        else:
            self.__chips -= chips
            self.__betted += chips
        self.__thinking = False
        self.__thinked = True

    def test(self, cards):
        card_list = []
        for i in self.__cards + cards:
            card_list.append(list(i.get_card))
        return print(card_list)

    def my_rank(self, cards):
        card_list = []
        for i in self.__cards + cards:
            card_list.append(list(i.get_card))
        self.__rank = s.get_rank(s.str_to_int(card_list))
        return self.__rank

    def community_rank(self, cards):
        card_list = []
        for i in cards:
            card_list.append(list(i.get_card))
        self.__rank = s.get_rank(s.str_to_int(card_list))
        return s.get_rank(s.str_to_int(card_list))

    def portential_community_rank(self, cards):
        card_list = []
        for i in cards:
            card_list.append(list(i.get_card))
        return s.get_potential_rank(s.str_to_int(card_list))

    @property
    def get_thinking(self):
        return self.__thinking

    def think(self, cards, step, bet_state, p_chips): # p_chips 은 플레이어1의 칩개수.
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
        #### 베팅할때 플레이어 1의 칩 개수를 넘기면 안됨. ####
        self.__thinking = True
        if step == 1:
            c_tree = self.community_rank(cards[:3])
            tree = self.my_rank(cards[:3])
            P_c_tree = self.portential_community_rank(cards[:3])
        elif step == 2:
            c_tree = self.community_rank(cards[:4])
            tree = self.my_rank(cards[:4])
            P_c_tree = self.portential_community_rank(cards[:4])
        else:
            c_tree = self.community_rank(cards)           # 투페어이상 해당 step2부터 사용
            tree = self.my_rank(cards)
            P_c_tree = self.portential_community_rank(cards)             # 스트레이트와 플러쉬만 해당 step 4부터 사용
        betting = [10, 10, 10, 10, 20, 20, 20, 30, 30, 50, 50, 100]
        rand = random.randint(1,100)
        bluffing = random.randint(1,random.randint(50,100))
        bluffing_list = [50, 50, 50, 100, 100, 200, 300]
        expected = bet_state - self.__betted

        # 쥐잡기
        print(bet_state)
        print(step)
        print(expected)
        print(self.__betted)


        # 배팅
        if step == 1:
            if tree in ("High_Card", "One_Pair"):
                if bet_state < 100:
                    if 10 < rand <= 90:
                        if expected <= 100:
                            self.bet(expected)
                        else:
                            if 30 < rand <= 70:
                                self.bet(expected)
                            else:
                                self.bet(-1)
                    else:
                        self.bet(-1)
                else:
                    if 30 < rand <= 70:
                        self.bet(expected)
                    else:
                        self.bet(-1)
            else:
                self.bet(expected)

        elif step == 2:
            if tree[1] == "High_Card":
                if bet_state < 100:
                    if 40 < bluffing <= 70:
                        if expected + 100 > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + 100)
                    else:
                        if 20 < rand <= 80:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                else:
                    if 40 < bluffing <= 70:
                        if expected + 100 > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + 100)
                    else:
                        self.bet(-1)
            elif tree[1] == "One_Pair":
                if bet_state < 150:
                    if 40 < bluffing <= 70:
                        random.shuffle(bluffing_list)
                        if expected + bluffing_list[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + bluffing_list[0])
                    else:
                        if 10 < rand <= 90:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                else:
                    if 40 < bluffing <= 70:
                        random.shuffle(bluffing_list)
                        if expected + bluffing_list[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + bluffing_list[0])
                    else:
                        self.bet(-1)
            elif tree[1] == "Two_Pair":
                if 40 < bluffing <= 70:
                    random.shuffle(bluffing_list)
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if c_tree[1] == "Two_Pair":
                        if 30 < rand <= 70:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                    else:
                        random.shuffle(betting)
                        if expected + betting[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + betting[0])
            elif tree[1] == "Triple":
                if 40 < bluffing <= 70:
                    random.shuffle(bluffing_list)
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if c_tree[1] == "Triple":
                        if 30 < rand <= 70:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                    else:
                        random.shuffle(betting)
                        if expected + betting[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + betting[0])
            else:
                if 40 < bluffing <= 70:
                    random.shuffle(bluffing_list)
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    random.shuffle(betting)
                    if expected + betting[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + betting[0])
        elif step == 3:
            if tree[1] == "High_Card":
                if bet_state < 100:
                    if 40 < bluffing <= 70:
                        if expected + 100 > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + 100)
                    else:
                        if 20 < rand <= 80:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                else:
                    if 40 < bluffing <= 70:
                        if expected + 100 > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + 100)
                    else:
                        self.bet(-1)
            elif tree[1] == "One_Pair":
                if bet_state < 150:
                    if 40 < bluffing <= 70:
                        random.shuffle(bluffing_list)
                        if expected + bluffing_list[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + bluffing_list[0])
                    else:
                        if 10 < rand <= 90:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                else:
                    if 40 < bluffing <= 70:
                        random.shuffle(bluffing_list)
                        if expected + bluffing_list[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + bluffing_list[0])
                    else:
                        self.bet(-1)
            elif tree[1] == "Two_Pair":
                if 40 < bluffing <= 70:
                    random.shuffle(bluffing_list)
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if c_tree[1] == "Two_Pair":
                        if 30 < rand <= 70:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                    else:
                        random.shuffle(betting)
                        if expected + betting[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + betting[0])
            elif tree[1] == "Triple":
                if 40 < bluffing <= 70:
                    random.shuffle(bluffing_list)
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if c_tree[1] == "Triple":
                        if 30 < rand <= 70:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                    else:
                        random.shuffle(betting)
                        if expected + betting[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + betting[0])
            elif tree[1] == "Straight":
                if 40 < bluffing <= 70:
                    random.shuffle(bluffing_list)
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if c_tree[1] == "Straight":
                        if 30 < rand <= 70:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                    else:
                        random.shuffle(betting)
                        if expected + betting[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + betting[0])
            elif tree[1] == "Flush":
                if 40 < bluffing <= 70:
                    random.shuffle(bluffing_list)
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if c_tree[1] == "Flush":
                        if 30 < rand <= 70:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                    else:
                        random.shuffle(betting)
                        if expected + betting[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + betting[0])
            elif tree[1] == "Full_House":
                if 40 < bluffing <= 70:
                    random.shuffle(bluffing_list)
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if c_tree[1] == "Flush":
                        if 30 < rand <= 70:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                    else:
                        random.shuffle(betting)
                        if expected + betting[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + betting[0])

        elif step == 4:
            if 40 < bluffing <= 70:
                random.shuffle(bluffing_list)
                if expected + bluffing_list[0] > p_chips:
                    self.bet(p_chips)
                else:
                    self.bet(expected + bluffing_list[0])
            else:
                if tree[1] == "Straight":
                    if P_c_tree == "P_Straight":
                        s_betting = [10, 20, 30, 50]
                        random.shuffle(s_betting)
                        if expected + s_betting[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + s_betting[0])
                    else:
                        random.shuffle(betting)
                        if expected + betting[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + betting[0])
                elif tree[1] == "Flush":
                    if P_c_tree == "P_Flush":
                        s_betting = [10, 20, 30, 50]
                        random.shuffle(s_betting)
                        if expected + s_betting[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + s_betting[0])
                    else:
                        random.shuffle(betting)
                        if expected + betting[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + betting[0])
                elif tree[1] in ("Two_Pair", "Triple", "Full_House", "Straight_Flush", "Royal_Flush"):
                    random.shuffle(betting)
                    if expected + betting[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + betting[0])
                else:
                    if bet_state < 100:
                        self.bet(expected)
                    else:
                        if 25 < rand < 75:
                            self.bet(expected)
                        else:
                            self.bet(-1)

        elif step == 5:
            if tree[1] in ("Triple", "Straight", "Flush", "Full_House", "Straight_Flush", "Royal_Flush"):
                self.bet(expected)
            else:
                if bet_state < 100:
                    self.bet(expected)
                else:
                    if 25 <  rand < 75:
                        self.bet(expected)
                    else:
                        self.bet(-1)


        if self.__chips < 0:
            s.bet_state += self.__chips
            self.__chips = 0

        if s.bet_state < self.__betted:
            s.bet_state = self.__betted
            s.bet_turn = s.bet_turn + 1 if s.bet_turn + 1 <= s.max_player else 1

        self.get__thinked = True