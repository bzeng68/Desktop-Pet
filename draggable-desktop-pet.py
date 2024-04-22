import random
import tkinter as tk
import os
import sys

# keeps track of position of the desktop pet and
# status of desktop pet (grabbed/doing action)
class DesktopPetManager:
    def __init__(self, x, y, grabbed, doing_action):
        self.x = x
        self.y = y
        self.grabbed = grabbed
        self.doing_action = doing_action
    
    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y
    
    def set_grabbed(self, grabbed):
        self.grabbed = grabbed

    def set_doing_action(self, doing_action):
        self.doing_action = doing_action

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_grabbed(self):
        return self.grabbed
    
    def get_doing_action(self):
        return self.doing_action

# util method
def resource_path(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)

# randomly determines actions the bear is allowed to do given the low and high constraints
# as well as positioning + movement constraints (so he doesn't walk off the screen)
def determine_action(low, high):
    if not desktopPetManager.get_grabbed() and not desktopPetManager.get_doing_action():
        action_const = actions_list[random.randrange(low, high + 1, 1)]
        next_action_range = possible_next_actions[action_const]

        if not can_walk_left() and action_const == WALK_NEG_CONST:
            action_const, next_action_range = reroll(WALK_NEG_CONST, next_action_range[0], next_action_range[1])
        
        if not can_walk_right() and action_const == WALK_POS_CONST:
            action_const, next_action_range = reroll(WALK_POS_CONST, next_action_range[0], next_action_range[1])

        movement_diff = 0
        if action_const == WALK_NEG_CONST:
            movement_diff = -6
        elif action_const == WALK_POS_CONST:
            movement_diff = 6

        desktopPetManager.set_doing_action(True)
        window.after(1, do_action, 0, action_const, movement_diff, next_action_range)

# recursively goes through frames of each gif, simulating bear doing actions
def do_action(curr_frame_num, action_const, movement_diff, next_action_range):
    if not desktopPetManager.get_grabbed():
        curr_frame = actions[action_const][curr_frame_num]
        desktopPetManager.set_x(desktopPetManager.get_x() + movement_diff)
        window.geometry(str(bear_dimension)+'x'+str(bear_dimension)+'+'+str(desktopPetManager.get_x())+'+'+str(desktopPetManager.get_y()))
        label.config(image = curr_frame)
        label.pack()

        wait_time = time_between_frame[action_const]
        if curr_frame_num < len(actions[action_const]) - 1: # if action has more frames to go
            window.after(wait_time, do_action, curr_frame_num + 1, action_const, movement_diff, next_action_range)
        else: # no more frames, determine next action
            desktopPetManager.set_doing_action(False)
            window.after(1, determine_action, next_action_range[0], next_action_range[1])
    else: # desktop pet is currently grabbed, so not doing action
        desktopPetManager.set_doing_action(False)

# simulates simple gravity based on if the bear is above ground level
def gravity():
    if desktopPetManager.get_y() < window_height - bear_dimension - 36:
        desktopPetManager.set_y(desktopPetManager.get_y() + 2)
        label.config(image = actions[FALLING_CONST])
        window.geometry(str(bear_dimension)+'x'+str(bear_dimension)+'+'+str(desktopPetManager.get_x())+'+'+str(desktopPetManager.get_y()))
        window.after(1, gravity)
    else: # when bear has reached ground level, call landing to show landing animation
        window.after(1, landing, 0)

# recursively iterates through the frames of the landing gif, simulating bear landing
# calls determine_action once animation is done
def landing(frame_num):
    label.config(image = actions[LANDING_CONST][frame_num])
    if frame_num < len(actions[LANDING_CONST]) - 1:
        window.after(time_between_frame[LANDING_CONST], landing, frame_num + 1)
    else:
        window.after(1, determine_action, 0, 0)

# when bear is grabbed, update image of bear and boolean of desktop pet manager
# also record x and y offset from top left corner of image (used during drag_motion)
def drag_start(event):
    desktopPetManager.set_grabbed(True)
    label.config(image = actions[GRABBED_CONST])
    widget = event.widget
    widget.rel_x = event.x
    widget.rel_y = event.y

# continuously updates the desktopPetManager with accurate x and y values for the bear
# and places the bear at the new x and y position
def drag_motion(event):
    widget = event.widget
    new_x = event.x_root - widget.rel_x
    new_y = event.y_root - widget.rel_y
    desktopPetManager.set_x(new_x)
    desktopPetManager.set_y(new_y)
    window.geometry(str(bear_dimension)+'x'+str(bear_dimension)+'+'+str(desktopPetManager.get_x())+'+'+str(new_y))

# update desktopPetManager and call gravity, if bear is on ground, gravity func will handle
def drag_end(event):
    desktopPetManager.set_grabbed(False)
    window.after(1, gravity)

# determines if bear can walk left w/o leaving screen
def can_walk_left():
    return (desktopPetManager.get_x() - 36) > 0

# determines if bear can walk right w/o leaving screen
def can_walk_right():
    return (desktopPetManager.get_x() + bear_dimension + 36) < window_width

# keeps randomly rolling different actions until the action doesn't match the given restricted one
def reroll(restricted_action_const, low, high):
    rolled_action_const = actions_list[random.randrange(low, high + 1, 1)]
    
    while rolled_action_const == restricted_action_const:
        rolled_action_const = actions_list[random.randrange(low, high + 1, 1)]

    return rolled_action_const, possible_next_actions[rolled_action_const]

# constants to help keep track of actions and states
IDLE_CONST = 'idle'
ITS_CONST = 'idle_to_sleep'
SLEEP_CONST = 'sleep'
STI_CONST = 'sleep_to_idle'
HEART_CONST = 'heart'
WALK_POS_CONST = 'walk_positive'
WALK_NEG_CONST = 'walk_negative'
GRABBED_CONST = 'grabbed'
LANDING_CONST = 'landing'
FALLING_CONST = 'falling'

# list of actions with varying frequencies, used for determining which action
# to do next. more frequent, more likely to happen
actions_list = [IDLE_CONST, IDLE_CONST, # 0, 1
                HEART_CONST, HEART_CONST, # 2, 3
                WALK_POS_CONST, WALK_POS_CONST, # 4, 5
                WALK_NEG_CONST, WALK_NEG_CONST, # 6, 7
                ITS_CONST, # 8
                SLEEP_CONST, SLEEP_CONST, SLEEP_CONST, SLEEP_CONST, SLEEP_CONST, # 9, 10, 11, 12, 13
                STI_CONST]

# time between each frame for different actions
time_between_frame = {IDLE_CONST: 500,
                      HEART_CONST: 500,
                      WALK_POS_CONST: 500,
                      WALK_NEG_CONST: 500,
                      ITS_CONST: 100,
                      SLEEP_CONST: 1000,
                      STI_CONST: 100,
                      LANDING_CONST: 50}

# range for possible nexxt action based on current action
possible_next_actions = {IDLE_CONST: (0, 8),
                         HEART_CONST: (0, 8),
                         WALK_POS_CONST: (0, 8),
                         WALK_NEG_CONST: (0, 8),
                         ITS_CONST: (9, 9), # must sleep after sitting down
                         SLEEP_CONST: (9, 14), # 80% to sleep, 20% to wake
                         STI_CONST: (0, 0)} # must idle after getting up

window = tk.Tk() # default window, the background
window_width = window.winfo_screenwidth()
window_height = window.winfo_screenheight()

# initialize desktopPetManager and bear_dimension or size
bear_dimension = 96
desktopPetManager = DesktopPetManager(window_width - bear_dimension - 36, window_height - bear_dimension - 52, False, False)
bear_96_prefix = '96px_bears'
bear_96_suffix = '_96'

IDLE_PATH = '{0}\\idle{1}.gif'.format(bear_96_prefix, bear_96_suffix)
HEART_PATH = '{0}\\heart{1}.gif'.format(bear_96_prefix, bear_96_suffix)
WALK_POS_PATH = '{0}\\walking_positive{1}.gif'.format(bear_96_prefix, bear_96_suffix)
WALK_NEG_PATH = '{0}\\walking_negative{1}.gif'.format(bear_96_prefix, bear_96_suffix)
ITS_PATH = '{0}\\idle_to_sleep{1}.gif'.format(bear_96_prefix, bear_96_suffix)
SLEEP_PATH = '{0}\\sleep{1}.gif'.format(bear_96_prefix, bear_96_suffix)
STI_PATH = '{0}\\sleep_to_idle{1}.gif'.format(bear_96_prefix, bear_96_suffix)
GRABBED_PATH = '{0}\\grabbed_bear{1}.png'.format(bear_96_prefix, bear_96_suffix)
LANDING_PATH = '{0}\\landing_bear{1}.gif'.format(bear_96_prefix, bear_96_suffix)
FALLING_PATH = '{0}\\falling_bear{1}.png'.format(bear_96_prefix, bear_96_suffix)

# actions and their respective gifs
actions = {IDLE_CONST: [tk.PhotoImage(file=resource_path(IDLE_PATH), format='gif -index %i' % (i)) for i in range(5)],
           HEART_CONST: [tk.PhotoImage(file=resource_path(HEART_PATH), format='gif -index %i' % (i)) for i in range(4)],
           WALK_POS_CONST: [tk.PhotoImage(file=resource_path(WALK_POS_PATH), format='gif -index %i' % (i)) for i in range(6)], # walk to right
           WALK_NEG_CONST: [tk.PhotoImage(file=resource_path(WALK_NEG_PATH), format='gif -index %i' % (i)) for i in range(6)], # walk to left
           ITS_CONST: [tk.PhotoImage(file=resource_path(ITS_PATH), format='gif -index %i' % (i)) for i in range(5)],
           SLEEP_CONST: [tk.PhotoImage(file=resource_path(SLEEP_PATH), format='gif -index %i' % (i)) for i in range(4)],
           STI_CONST: [tk.PhotoImage(file=resource_path(STI_PATH), format='gif -index %i' % (i)) for i in range(6)],
           GRABBED_CONST: tk.PhotoImage(file=resource_path(GRABBED_PATH)),
           LANDING_CONST: [tk.PhotoImage(file=resource_path(LANDING_PATH), format='gif -index %i' % (i)) for i in range(5)],
           FALLING_CONST: tk.PhotoImage(file=resource_path(FALLING_PATH))}

label = tk.Label(window, bg='black', width = bear_dimension, height = bear_dimension) # label is what the frame of the gif gets put on
window.overrideredirect(True) # hide tkinter gui outline
window.config(background='black')
window.wm_attributes('-transparentcolor', 'black') # black background now turned to transparent
window.wm_attributes('-topmost', True)
window.geometry(str(bear_dimension)+'x'+str(bear_dimension)+'+'+str(desktopPetManager.get_x())+'+'+str(desktopPetManager.get_y())) #initial placement, bottom right

label.bind('<Button-1>', drag_start) # when label is first grabbed, call drag_start
label.bind('<B1-Motion>', drag_motion) # when label is being dragged around, call drag_motion
label.bind('<ButtonRelease-1>', drag_end) # when label is released, call drag_end

window.after(1, determine_action, 0, 0) # first call, starts cycle of bear action

window.mainloop()