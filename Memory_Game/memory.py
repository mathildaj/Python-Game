# implementation of card game - Memory

import simplegui
import random
import math

#declare global variables
cards = []
exposed = []
state = 0
first_card = 0
second_card = 0
turns = 0

#initialize the cards and exposed
cards_1 = []
for n in range(8):
    cards_1.append(n)
    
cards = cards_1 + cards_1

for i in range(16):
        exposed.append(False)
    
# helper function to initialize globals
def new_game():
    global cards, exposed, state, turns
    
    state = 0
    turns = 0
    
    random.shuffle(cards)
    #print cards
    
    for i in range(16):
        exposed[i] = False
    
       
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, first_card, second_card, turns
    
    # find out which card the mouse clicks on
    card_index = pos[0] // 50
    
    if exposed[card_index] == True:
        pass # ignore the mouse click
    else:
        exposed[card_index] = True
        if state == 0:
            turns += 1
            state = 1
            first_card = card_index
        elif state == 1:
            state = 2
            second_card = card_index
        else:
            if cards[first_card] != cards[second_card]:
                exposed[first_card] = False
                exposed[second_card]= False
               
            state = 1
            turns += 1
            first_card = card_index
           
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global turns
    for card_index in range(len(cards)):
        card_pos = 50 * card_index
        if exposed[card_index] == True:
            canvas.draw_polygon(
                [[card_index * 50, 0],
                [(card_index + 1) * 50, 0],
                [(card_index + 1) * 50, 100],
                [card_index * 50, 100]],
                1, "Yellow", "Black")
            canvas.draw_text(str(cards[card_index]), (card_pos,50), 40, "White")
        else:
            canvas.draw_polygon(
                [[card_index * 50, 0],
                [(card_index + 1) * 50, 0],
                [(card_index + 1) * 50, 100],
                [card_index * 50, 100]],
                1, "Yellow", "Green")
    
    label.set_text("Turns =  " + str(turns))

            
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


