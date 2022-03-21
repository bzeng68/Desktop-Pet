import pyautogui
import random
import tkinter as tk
import os
import sys

cycle = 0
check = 1
idle_num = [1, 2]
heart_num = [6, 7]  # 5 is idle to sleep
sleep_num = [10, 11, 12, 13, 15]  # 14 is sleep to idle
walk_pos_num = [8, 9]
walk_neg_num = [3, 4]
event_number = random.randrange(1, 3, 1)

window = tk.Tk()
window_width = window.winfo_screenwidth()
window_height = window.winfo_screenheight()

x = window_width


def resource_path(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)


idle = [tk.PhotoImage(file=resource_path('idle.gif'),
                      format='gif -index %i' % (i)) for i in range(5)]
idle_to_sleep = [tk.PhotoImage(
    file=resource_path('idle_to_sleep.gif'), format='gif -index %i' % (i)) for i in range(5)]
sleep = [tk.PhotoImage(file=resource_path('sleep.gif'),
                       format='gif -index %i' % (i)) for i in range(4)]
sleep_to_idle = [tk.PhotoImage(
    file=resource_path('sleep_to_idle.gif'), format='gif -index %i' % (i)) for i in range(6)]
heart = [tk.PhotoImage(
    file=resource_path('heart.gif'), format='gif -index %i' % (i)) for i in range(4)]
walk_positive = [tk.PhotoImage(file=resource_path('walking_positive.gif'),
                               format='gif -index %i' % (i)) for i in range(6)]  # walk to left
walk_negative = [tk.PhotoImage(file=resource_path('walking_negative.gif'),
                               format='gif -index %i' % (i)) for i in range(6)]  # walk to right


def gif_work(cycle, frames, event_number, first_num, last_num):
    if cycle < len(frames) - 1:
        cycle = cycle + 1
    else:
        cycle = 0
        event_number = random.randrange(first_num, last_num + 1, 1)
    return cycle, event_number


def update(cycle, check, event_number, x):
    if check == 0:
        frame = idle[cycle]
        cycle, event_number = gif_work(cycle, idle, event_number, 1, 9)

    elif check == 1:
        frame = idle_to_sleep[cycle]
        cycle, event_number = gif_work(
            cycle, idle_to_sleep, event_number, 10, 10)

    elif check == 2:
        frame = sleep[cycle]
        cycle, event_number = gif_work(
            cycle, sleep, event_number, 10, 15)

    elif check == 3:
        frame = sleep_to_idle[cycle]
        cycle, event_number = gif_work(
            cycle, sleep_to_idle, event_number, 1, 1)

    elif check == 4:
        frame = heart[cycle]
        cycle, event_number = gif_work(
            cycle, heart, event_number, 1, 9)

    elif check == 5:
        if x - 36 < 0:
            frame = heart[cycle]
            cycle, event_number = gif_work(
                cycle, heart, event_number, 1, 9)
        else:
            frame = walk_positive[cycle]
            cycle, event_number = gif_work(
                cycle, walk_positive, event_number, 1, 9)
            x -= 6

    elif check == 6:
        if x + 292 > window_width:
            frame = heart[cycle]
            cycle, event_number = gif_work(
                cycle, heart, event_number, 1, 9)
        else:
            frame = walk_negative[cycle]
            cycle, event_number = gif_work(
                cycle, walk_negative, event_number, 1, 9)
            x += 6
    window.geometry('256x256+'+str(x - 286) +
                    '+'+str(window_height - 316))
    label.config(image=frame)
    label.pack()
    window.after(1, event, cycle, check, event_number, x)


def event(cycle, check, event_number, x):
    if event_number in idle_num:
        check = 0
        window.after(400, update, cycle, check, event_number, x)

    elif event_number == 5:
        check = 1
        window.after(100, update, cycle, check, event_number, x)

    elif event_number in heart_num:
        check = 4
        window.after(400, update, cycle, check, event_number, x)

    elif event_number in sleep_num:
        check = 2
        window.after(1000, update, cycle, check, event_number, x)

    elif event_number in walk_pos_num:
        check = 5
        window.after(500, update, cycle, check, event_number, x)

    elif event_number in walk_neg_num:
        check = 6
        window.after(500, update, cycle, check, event_number, x)

    elif event_number == 14:
        check = 3
        window.after(100, update, cycle, check, event_number, x)


if (os.name == "nt"):
    window.config(highlightbackground='black')
    label = tk.Label(window, bg='black')
    window.overrideredirect(True)
    window.wm_attributes('-transparentcolor', 'black')
    window.wm_attributes('-topmost', True)
else:
    label = tk.Label(window)
    label.config(bg='systemTransparent')
    window.overrideredirect(True)
    window.wm_attributes('-topmost', True)
    window.wm_attributes('-transparent', True)

window.after(1, update, cycle, check, event_number, x)

window.mainloop()
