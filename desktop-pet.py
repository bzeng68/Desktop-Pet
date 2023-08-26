import random
import tkinter as tk
import os
import sys

def resource_path(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)

def determine_action(low, high, x):
    action_const = actions_list[random.randrange(low, high + 1, 1)]
    next_action_range = possible_next_actions[action_const]

    movement_diff = 0
    if action_const == WALK_POS_CONST:
        movement_diff = -6
    elif action_const == WALK_NEG_CONST:
        movement_diff = 6

    if not grabbed:
        window.after(1, do_action, 0, action_const, movement_diff, x, next_action_range)

def do_action(curr_frame_num, action_const, movement_diff, x, next_action_range):
    if not grabbed:
        curr_frame = actions[action_const][curr_frame_num]
        x += movement_diff
        window.geometry('256x256+'+str(x - 286) +
                        '+'+str(window_height - 316))
        label.config(image = curr_frame)
        label.pack()

        wait_time = time_between_frame[action_const]
        if curr_frame_num < len(actions[action_const]) - 1: # if action has more frames to go
            window.after(wait_time, do_action, curr_frame_num + 1, action_const, movement_diff, x, next_action_range)
        else:
            window.after(1, determine_action, next_action_range[0], next_action_range[1], x)

grabbed = False

IDLE_CONST = 'idle'
ITS_CONST = 'idle_to_sleep'
SLEEP_CONST = 'sleep'
STI_CONST = 'sleep_to_idle'
HEART_CONST = 'heart'
WALK_POS_CONST = 'walk_positive'
WALK_NEG_CONST = 'walk_negative'

# list of actions with varying frequencies, used for determining which action
# to do next. more frequent, more likely to happen
actions_list = [IDLE_CONST, IDLE_CONST, # 0, 1
                HEART_CONST, HEART_CONST, # 2, 3
                WALK_POS_CONST, WALK_POS_CONST, # 4, 5
                WALK_NEG_CONST, WALK_NEG_CONST, # 6, 7
                ITS_CONST, # 8
                SLEEP_CONST, SLEEP_CONST, SLEEP_CONST, SLEEP_CONST, SLEEP_CONST, # 9, 10, 11, 12, 13
                STI_CONST] # 14

# time between each frame for different actions
time_between_frame = {IDLE_CONST: 500,
                      HEART_CONST: 500,
                      WALK_POS_CONST: 500,
                      WALK_NEG_CONST: 500,
                      ITS_CONST: 100,
                      SLEEP_CONST: 1000,
                      STI_CONST: 100}

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

x = window_width

# actions and their respective gifs
actions = {IDLE_CONST: [tk.PhotoImage(file=resource_path('idle.gif'), format='gif -index %i' % (i)) for i in range(5)],
           HEART_CONST: [tk.PhotoImage(file=resource_path('heart.gif'), format='gif -index %i' % (i)) for i in range(4)],
           WALK_POS_CONST: [tk.PhotoImage(file=resource_path('walking_positive.gif'), format='gif -index %i' % (i)) for i in range(6)],  # walk to left
           WALK_NEG_CONST: [tk.PhotoImage(file=resource_path('walking_negative.gif'), format='gif -index %i' % (i)) for i in range(6)],
           ITS_CONST: [tk.PhotoImage(file=resource_path('idle_to_sleep.gif'), format='gif -index %i' % (i)) for i in range(5)],
           SLEEP_CONST: [tk.PhotoImage(file=resource_path('sleep.gif'), format='gif -index %i' % (i)) for i in range(4)],
           STI_CONST: [tk.PhotoImage(file=resource_path('sleep_to_idle.gif'), format='gif -index %i' % (i)) for i in range(6)]}  # walk to right

if (os.name == "nt"):
    window.config(highlightbackground='black')
    label = tk.Label(window, bg='black') # label is what the frame of the gif gets put on
    window.overrideredirect(True)
    window.wm_attributes('-transparentcolor', 'black')
    window.wm_attributes('-topmost', True)
else:
    label = tk.Label(window)
    label.config(bg='systemTransparent')
    window.overrideredirect(True)
    window.wm_attributes('-topmost', True)
    window.wm_attributes('-transparent', True)

window.after(1, determine_action, 0, 0, x)

window.mainloop()
