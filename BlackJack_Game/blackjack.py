# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        str_hand = ""
        for card in self.cards:
            str_hand += " " + card.__str__()
        return "Hand contains: " + str_hand
            

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        has_ace = False
        
        for card in self.cards:
            value += VALUES[card.get_rank()]
        for card in self.cards:
            if card.get_rank() == 'A':
                has_ace = True
                break
        if has_ace == True:
            if value + 10 <= 21:
                value += 10
                
        return value
    
    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 80
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
        

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0)
    
    def __str__(self):
        str_deck = ""
        for card in self.cards:
            str_deck += " " + card.__str__()
        return "Deck contains: " + str_deck



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score
    
    if in_play == True:
        outcome = "Player lost! New deal?"
        score -= 1
    else:
        outcome = "Player, hit or stand?"
        
    deck = Deck()
    deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()
    
    for i in range(2):
        player_hand.add_card(deck.deal_card())
    for i in range(2):
        dealer_hand.add_card(deck.deal_card())
    
    in_play = True

def hit():
    global in_play, outcome, score
    # if the hand is in play, hit the player
    if in_play == True:
        player_hand.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:
        outcome = "Player busted! New deal?"
        in_play = False
        score -= 1
       
def stand():
    global in_play, outcome, score   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
                outcome = "Dealer busted! New deal?"
                in_play = False
                score += 1
        elif player_hand.get_value() > 21:
            outcome = "Dealer busted! New deal?"
            in_play = False
            score -= 1
        elif dealer_hand.get_value()>= player_hand.get_value():
            outcome = "Dealer won!  New deal?"
            score -= 1
            in_play = False
        else:
            outcome = "Player won! New deal?"
            score += 1
            in_play = False
            
             
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])
    
    canvas.draw_text("Blackjack", [220, 50], 50 ,"Pink")
    canvas.draw_text("Dealer:", [10, 150], 25, "Black") 
    canvas.draw_text("Player:", [10, 300], 25, "Black") 
    

    player_hand.draw(canvas, [100, 300])
    dealer_hand.draw(canvas, [100, 150])

    canvas.draw_text(outcome, [10, 100], 25 ,"Pink")
    
    canvas.draw_text("Score: " + str(score), [400, 90], 30 ,"Black")
    

    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (136,199), CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


