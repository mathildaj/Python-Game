"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
import math
#import poc_holds_testsuite
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set



def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    scores = [hand.count(num) * num for num in hand]
    return max(scores)
    

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = ([dummy_num for dummy_num in range(1, num_die_sides+1)])
    all_free_seqs = gen_all_sequences(outcomes, num_free_dice)
    sum_value = 0
    for seq in all_free_seqs:
        sum_value += score(seq + held_dice)
    
    #print all_free_seqs    
    #print free_dice_prob
    #print free_dice_value
    #print held_dice_value
    #print held_dice_value + free_dice_value
    
    return sum_value / float(len(all_free_seqs))


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    
    answer_set = set([()])
    for dummy_idx in range(len(hand)):
        temp_set = set()
        for partial_sequence in answer_set:
            new_sequence = list(partial_sequence)
            new_sequence.append(hand[dummy_idx])
            temp_set.add(tuple(new_sequence))
        answer_set = answer_set.union(temp_set)
    return answer_set



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    return_dict = {}
    
    all_holds = gen_all_holds(hand)
    for hold in all_holds:
        num_free_dice = len(hand) - len(hold)
        new_value = expected_value(hold, num_die_sides,num_free_dice)
        return_dict[new_value] = hold
    max_value = max([value for value in return_dict])    
        
    return (max_value, return_dict[max_value])


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#test score function
#hand = (6,5,5,6,1)
#print score(hand)
#test expected_value
#held_dice = (1,1)
#expected_value(held_dice,6, 1)

#poc_holds_testsuite.run_suite(gen_all_holds)
    
    
    



