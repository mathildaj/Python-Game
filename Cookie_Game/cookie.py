"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self, total_cookies=0.0, current_cookies=0.0, 
                 current_time=0.0, current_cps=1.0): 
                 
        """
        initialize the class
        """
        self._total_cookies = total_cookies
        self._current_cookies = current_cookies
        self._current_time = current_time #in seconds
        self._current_cps = current_cps #cookies per second
        self._history = []
        self._history.append((0.0, None, 0.0, 0.0))
        
    def __str__(self):
        """
        Return human readable state
        """
        return_str = "Time: " + str(self._current_time) + "\n"
        return_str += "Current Cookies: " + str(self._current_cookies) + "\n"
        return_str +=  "CPS: " + str(self._current_cps) + "\n"
        return_str += "Total Cookies: " + str(self._total_cookies) + "\n"
        
        return return_str
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history[:]

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies >= cookies:
            return 0.0
        else:
            return math.ceil((cookies - self._current_cookies) / self._current_cps)
        
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._current_time += time
            self._current_cookies += time * self._current_cps
            self._total_cookies += time * self._current_cps
            
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, 
                                 item_name, 
                                 cost, 
                                 self._total_cookies))
           
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    
    info = build_info.clone()
    clicker_state = ClickerState()
   
    while duration >= 0:
        current_cookies = clicker_state.get_cookies()
        current_cps = clicker_state.get_cps()
        current_history = clicker_state.get_history()
                
        build_item = strategy(current_cookies,
                              current_cps,
                              current_history,
                              duration,
                              info)
        if build_item == None:
            break
        item_cost = info.get_cost(build_item)
        add_cps = info.get_cps(build_item)
        wait_until_time = clicker_state.time_until(item_cost)
                                   
        if wait_until_time > duration:
            break;
        else:
            duration -= wait_until_time
            clicker_state.wait(wait_until_time)
            clicker_state.buy_item(build_item, item_cost, add_cps)
            info.update_item(build_item)
            
    clicker_state.wait(duration)
        
    return clicker_state    
        


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    total_cookies_to_have = cookies + cps * time_left
    cheapest_item = None
    cheapest_cost = total_cookies_to_have
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        if cost <= cheapest_cost:
            cheapest_cost = cost
            cheapest_item = item
    return cheapest_item       

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    total_cookies_to_have = cookies + cps * time_left
    expensive_item = None
    expensive_cost = 0.0
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        if cost >= expensive_cost and cost <= total_cookies_to_have:
            expensive_cost = cost
            expensive_item = item
    return expensive_item       

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    total_cookies_to_have = cookies + cps * time_left
    best_item = None
    best_ratio = 0.0
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        cps = build_info.get_cps(item)
        if (cps * 1.0 / cost) > best_ratio and cost <= total_cookies_to_have:
            best_ratio = cps * 1.0 / cost
            best_item = item
    return best_item       
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    run_strategy("Cursor", 500.0, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    #run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    
#test methods
#test init 
#new_state = ClickerState(5.0, 4.0, 60, 2.0)
#print "new_state._total_cookies= " + str(new_state._total_cookies)
#print "new_state._current_cookies= " + str(new_state._current_cookies)
#print "new_state._current_time= " + str(new_state._current_time)
#print "new_state._current_cps= " + str(new_state._current_cps)
#print "new_state._history = " + str(new_state._history)
#test __str__
#print new_state
#test time_until
#print new_state.time_until(2155)