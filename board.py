import numpy as np
import pandas as pd
from collections import defaultdict

class Square:
    def __init__(self, position, name):
        self.position = position
        self.name = name
        self.visits = 0

class Property(Square):
    def __init__(self, position, name, price):
        super().__init__(position, name)
        self.price = price
        self.rent = 0
        self.profit = 0
        self.owner = None
    def land_action(self, player):
        if not self.owner:
            player.consider(self)
        else:
            self.charge(player)
        self.visits += 1
    def charge(self, player):
        player.balance -= self.rent
        self.profit += self.rent
        self.owner.balance += self.rent

class Building(Property):
    def __init__(self, position, name, price, rents, color):
        super().__init__(position, name, price)
        self.rents = rents
        self.color = color
        
class Railroad(Property):
    def __init__(self, position, name):
        super().__init__(position, name, 200)
        self.rents = (25, 50, 100, 200)

class Utility(Property):
    def __init__(self, position, name):
        super().__init__(position, name, 150)
        self.rents = (4, 12)

class Tax(Square):
    def __init__(self, position, name, cost):
        super().__init__(position, name)
        self.cost = cost
    def land_action(self, player):
        player.balance -= self.cost
        self.visits += 1

class Go(Square):
    def __init__(self):
        super().__init__(0, "Go")
    def land_action(self, player):
        self.visits += 1

class Jail(Square):
    def __init__(self):
        super().__init__(10, "Jail")
    def land_action(self, player):
        self.visits += 1
        
class FreeParking(Square):
    def __init__(self):
        super().__init__(20, "Free Parking")
        self.balance = 0
        
class GoToJail(Square):
    def __init__(self):
        super().__init__(30, "Go To Jail")

class Chance(Square):
    def advance_to_boardwalk(player):
        player.update_position(39)
    def advance_to_go(player):
        player.update_position(0)
    def advance_to_illinois(player):
        player.update_position(24)
    def advance_to_railroad_1(player):
        if 6 <= player.position <= 15:
            player.update_position(15)
        elif 16 <= player.position <= 25:
            player.update_position(25)
        elif 26 <= player.position <= 35:
            player.update_position(35)
        else:
            player.update_position(5)
    def advance_to_railroad_2(player):
        if 6 <= player.position <= 15:
            player.update_position(15)
        elif 16 <= player.position <= 25:
            player.update_position(25)
        elif 26 <= player.position <= 35:
            player.update_position(35)
        else:
            player.update_position(5)
    def advance_to_reading(player):
        player.update_position(5)
    def advance_to_st_charles(player):
        player.update_position(11)
    def advance_to_utility(player):
        if 13 <= player.position <= 28:
            player.update_position(28)
        else:
            player.update_position(12)
    def back_three_spaces(player):
        player.update_position((player.position - 3) % 40)
        player.balance -= 200
    def bank_pays_dividend(player):
        player.balance += 50
    def building_loan_matures(player):
        player.balance += 150
    def chairman_of_board(player):
        player.balance -= 150
        board[20].balance += 150
    def get_out_of_jail(player):
        player.jailed = -1
    def go_to_jail(player):
        player.jailed += 1
        player.update_position(10)
    def property_repairs(player):
        for prop in player.properties:
            if type(prop) == Building:
                player.balance -= 25*prop.houses
                board[20].balance += 25*prop.houses
                player.balance -= 100*prop.hotels
                board[20].balance += 100*prop.hotels
    def speeding_fine(player):
        player.balance -= 15
        board[20].balance += 20
    
    all_cards = [
            advance_to_boardwalk, advance_to_go, advance_to_illinois, advance_to_railroad_1, advance_to_railroad_2,
            advance_to_reading, advance_to_st_charles, advance_to_utility, back_three_spaces, bank_pays_dividend, 
            building_loan_matures, chairman_of_board, get_out_of_jail, go_to_jail, property_repairs, speeding_fine
            ]
    
    active_cards = list(all_cards)
    
    def __init__(self, position, name):
        super().__init__(position, name)
    def land_action(self, player):
        card_index = np.random.choice(np.arange(len(active_cards)))
        chosen_card = active_cards.pop(card_index)
        chosen_card(player)
        if not active_cards:
            active_cards = self.all_cards
    
class CommunityChest(Square):
    def advance_to_go(player):
        player.update_position(0)
    def bank_error(player):
        player.balance += 200
    def beauty_contest(player):
        player.balance += 10
    def birthday(player):
        player.balance += 30
        board[20].balance -= 30
    def consultancy_fee(player):
        player.balance += 25
    def doctors_fee(player):
        player.balance -= 50
        board[20].balance += 50
    def get_out_of_jail(player):
        player.jailed = -1
    def go_to_jail(player):
        player.jailed += 1
        player.update_position(10)
    def holiday_fund_matures(player):
        player.balance += 100
    def hospital_fees(player):
        player.balance -= 100
    def income_tax_refund(player):
        player.balance += 20
        board[20].balance += 100
    def inherit_money(player):
        player.balance += 100
    def life_insurance_matures(player):
        player.balance += 100
    def school_fees(player):
        player.balance -= 50
        board[20].balance += 50
    def sell_stock(player):
        player.balance += 50
    def street_repairs(player):
        for prop in player.properties:
            if type(prop) == Building:
                player.balance -= 40*prop.houses
                board[20].balance += 40*prop.houses
                player.balance -= 115*prop.hotels
                board[20].balance += 115*prop.hotels

    all_cards = [
            advance_to_go, bank_error, beauty_contest, birthday, consultancy_fee, doctors_fee,
            get_out_of_jail, go_to_jail, holiday_fund_matures, hospital_fees, income_tax_refund, 
            inherit_money, life_insurance_matures, school_fees, sell_stock, street_repairs
            ]
    
    active_cards = list(all_cards)

    def __init__(self, position, name):
        super().__init__(position, name)
    def land_action(self, player):
        card_index = np.random.choice(np.arange(len(active_cards)))
        chosen_card = active_cards.pop(card_index)
        chosen_card(player)
        if not active_cards:
            active_cards = self.all_cards

class Player:
    def roll():
        die_1 = np.random.choice([1, 2, 3, 4, 5, 6])
        die_2 = np.random.choice([1, 2, 3, 4, 5, 6])
        return (die_1, die_2)
    
    def __init__(self, risk):
        self.risk = risk
        self.balance = 1500
        self.properties = []
        self.position = 0
        self.jailed = 0
        
    def consider(self, prop):
        if prop.price < self.balance * self.risk:
            self.balance -= prop.price
            prop.owner = self
            prop.profit = -(prop.price)
            prop.rent = prop.rents[0]
    
    def update_position(self, new_pos):
        if self.jailed <= 0 and new_pos < self.position:
            self.balance += 200
        self.position = new_pos
        board[new_pos].land_action(self)
            
    def take_turn(self):
        curr_roll = Player.roll()
        if self.jailed:
            if curr_roll[0] == curr_roll[1]:
                self.jailed = 0
            elif self.balance * self.risk >= 50 or self.jailed > 3:
                self.balance -= 50
                board[20].balance += 50
                self.jailed = 0
            else:
                self.jailed += 1
        else:
            self.update_position((self.position + sum(curr_roll)) % 40)
            num_doubles = 1
            while curr_roll[0] == curr_roll[1]:
                num_doubles += 1
                if num_doubles >= 3:
                    self.jailed += 1
                    self.update_position(10)
                    break
                curr_roll = Player.roll()
            self.update_position((self.position + sum(curr_roll)) % 40)

board = [
    Go(),
    Building(1, "Mediterranean Avenue", 60, (2, 10, 30, 90, 160, 250), "Purple"),
    CommunityChest(2, "Community Chest 1"),
    Building(3, "Baltic Avenue", 60, (4, 20, 60, 180, 320, 450), "Purple"),
    Tax(4, "Income Tax", 200),
    Railroad(5, "Reading Railroad"),
    Building(6, "Oriental Avenue", 100, (6, 30, 90, 270, 400, 550), "Light Blue"),
    Chance(7, "Chance 1"),
    Building(8, "Vermont Avenue", 100, (6, 30, 90, 270, 400, 550), "Light Blue"),
    Building(9, "Connecticut Avenue", 120, (8, 40, 100, 300, 450, 600), "Light Blue"),
    Jail(),
    Building(11, "St. Charles Place", 140, (10, 50, 150, 450, 625, 750), "Pink"),
    Utility(12, "Electric Company"),
    Building(13, "States Avenue", 140, (10, 50, 150, 450, 625, 750), "Pink"),
    Building(14, "Virginia Avenue", 160, (12, 60, 180, 500, 700, 900), "Pink"),
    Railroad(15, "Pennsylvania Railroad"),
    Building(16, "St. James Place", 180, (14, 70, 200, 550, 750, 950), "Orange"),
    CommunityChest(17, "Community Chest 2"),
    Building(18, "Tennessee Avenue", 180, (14, 70, 200, 550, 750, 950), "Orange"),
    Building(19, "New York Avenue", 200, (16, 80, 220, 600, 800, 1000), "Orange"),
    FreeParking(),
    Building(21, "Kentucky Avenue", 220, (18, 90, 250, 700, 875, 1050), "Red"),
    Chance(22, "Chance 2"),
    Building(23, "Indiana Avenue", 220, (18, 90, 250, 700, 875, 1050), "Red"),
    Building(24, "Illinois Avenue", 240, (20, 100, 300, 750, 925, 1100), "Red"),
    Railroad(25, "B&O Railroad"),
    Building(26, "Atlantic Avenue", 260, (22, 110, 330, 800, 975, 1150), "Yellow"),
    Building(27, "Ventnor Avenue", 260, (22, 110, 330, 800, 975, 1150), "Yellow"),
    Utility(28, "Water Works"),
    Building(29, "Marvin Gardens", 280, (24, 120, 360, 850, 1025, 1200), "Yellow"),
    GoToJail(),
    Building(31, "Pacific Avenue", 300, (26, 130, 390, 900, 1100, 1275), "Green"),
    Building(32, "North Carolina Avenue", 300, (26, 130, 390, 900, 1100, 1275), "Green"),
    CommunityChest(33, "Community Chest 3"),
    Building(34, "Pennsylvania Avenue", 320, (28, 150, 450, 1000, 1200, 1400), "Green"),
    Railroad(35, "Short Line Railroad"),
    Chance(36, "Chance 3"),
    Building(37, "Park Place", 350, (35, 175, 500, 1100, 1300, 1500), "Dark Blue"),
    Tax(38, "Luxury Tax", 75),
    Building(39, "Boardwalk", 400, (50, 200, 600, 1400, 1500, 2000), "Dark Blue")
]