# Assignment: Disappearing Text Writing App
"""
An online writing app where if you stop typing, your work will disappear.

For most writers, a big problem is writing block. Where you can't think of what to write and you can't write anything.

One of the most interesting solutions to this is a web app called
The Most Dangerous Writing App, an online text editor where if you stop writing, all your progress will be lost.

A timer will count down and when the website detects the user has not written anything in the last 5/10 seconds,
it will delete all the text they've written so far.

Try it out here:
https://www.squibler.io/dangerous-writing-prompt-app

You are going to build a desktop app that has similar functionality.
The design is up to you, but it should allow a user to type and if they stop for more than 5 seconds,
it should delete everything they've written so far.
"""

# Approach/Steps
"""
App? What software? Or using python?
GUI? Tkinter?? 

1. Allow user to input text
2. Activate a timer to keep track of duration that nothing is being typed; 
    (how to detect for keyboard input/check user input?) https://stackoverflow.com/questions/24072790/how-to-detect-key-presses
    (how to listen to all keys on keyboard)
    (detect no keyboard input for certain amount of time python)
    (tkinter check duration user didnt input anything)
3. Wipe screen through GUI (tkinter functions or otherwise)
How to clear text from textbox??? (Not on canvas so cant clear screen)
Or workaround: Allow user to type in textbox but it shows on canvas instead?
Use .x_forget to hide label

References: 
>>Tkinter download font --pyglet font url redirect (https://pyglet.readthedocs.io/en/latest/modules/font.html)
>>Tkinter text input
>>Scary text font -Creepster
>>Tkinter change input text box size , font and color
>>Tkinter hide entry label background color
>>Tkinter hide button after click (https://stackoverflow.com/questions/53256356/hide-a-button-in-tkinter)
>>Tkinter stop currently running functions 
>>Tkinter disable all widgets in frame

Improvements:
Problem detecting no user input (solved) + stopping all running functions on stop button press
Output written text to text file?
Add save progress feature (Once button to stop is clicked)

ISSUE WITH EVENT LOOP; button event listener doesnt proc function consecutively at all (or simply ignores timer totally)
--Problem with layering orders for tkinter function 
    (try seperating into different functions so that it doesnt all get run at once)
--Is there main event loop in tkinter programs? https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
--Tkinter main loop doesnt work like python main loop; button is just event listener...
--GUI outputs everything at once regardless of line order of code
Spent too much time on font formatting; pyglet import font not working
Better plan the layout properly; struggling to put elements on the screen according to the desired outcome
Grid doesnt work properly; using place
"""
# GLARING ISSUES:
# Cant stop running current function calls (even with after_cancel)
# -- Causes parallel threads
# -- USE "return" to stop function calls
# -- CREATE OBJECTS AND RESET ALL TO NONE (window.after_cancel)
# Cant manage to show countdown for time before all text deleted (want it to appear on main timer)
# Want timer value to continue from last text deletion point instead of restarting from (15:00?) (fixed)
# pyglet import font not working


from tkinter import *
import pyglet, os
from pyglet import font
import math
import time
import keyboard

font.add_file('Creepster_Regular.ttf')
Creepster_Regular = font.load('Creepster Regular')

FONT_NAME = "Lucida Handwriting"
SCARY_FONT = font.add_file('Creepster_Regular.ttf')
PINK = "#ed594e"
BLOOD_RED = "#ff3838"
DARK_RED = "#5e1212"
BLACK = "#030202"
timer = None
time_out = False
count = 0
counter = 0
writing_time_limit = 0
writing_phase = 0
writing_stopped = False
compare_text = ""

# def writing_button_clicked(): #original intention was to deal with instant function calls but solved by splitting into diff functions
#     for i in range(3):
#         window.after(500, writing_has_begun)

"""def wait_for_user(secs):
    import msvcrt
    import time
    start = time.time()
    while True:
        if msvcrt.kbhit():
            msvcrt.getch()
            break
        if time.time() - start > secs:
            break
    return True"""

#TO PREVENT PARALLEL FUNCTION RUNS, CREATE ANOTHER SWITCH TO TAKE NOTE IF FUNCTION IS RUNNING OR NOT.
# TO FLIP SWITCH, FUNCTION RETURNS VALUE TO CHANGE STATE OF SWITCH
is_running_writing_has_begun_0 = False
is_running_writing_has_begun_1 = False
is_running_writing_has_begun_2 = False
countdown_switch = False

# writing_phase = 0
def writing_has_begun_0():
    # START BUTTON
    # >>Seperated into different functions to prevent instant function calls
    # Why does all the events proc simultaneously & ignoring the timer mechanism? (regardless of)
    # Need loop in main to keep proccing this function --> causes infinite loop
    # Just call itself

    global writing_phase, writing_stopped, count, time_out
    global is_running_writing_has_begun_0, is_running_writing_has_begun_1, is_running_writing_has_begun_2
    print(f"0 writing_phase: {writing_phase}")

    # Flip the switch to allow all functions to continue running. But why does the function calls continue from before instead of new state?
    is_running_writing_has_begun_0 = True
    writing_stopped = False
    time_out = False
    start_button.place_forget()
    stop_button.place(x=1000, y=650)

    # ------------TEXT INPUT----------------------#
    # Implement appearing text on screen at different intervals
    disappearing_text_label.config(text="")
    keep_writing_label.config(text="")
    regret_label.config(text="")

    # Countdown before showing starting text before user begins writing
    if writing_phase == 0:
        count_down(3,0)
        writing_phase += 1
    if writing_phase == 1:
        window.after(3000, writing_has_begun_1)
        is_running_writing_has_begun_1 = False
    elif writing_phase == 2:
        window.after(3000, writing_has_begun_2)
        is_running_writing_has_begun_2 = False

#writing_phase = 1
def writing_has_begun_1():
    global writing_phase, writing_stopped, is_running_writing_has_begun_1
    if not writing_stopped and not is_running_writing_has_begun_1:
        print(f"1 writing_phase: {writing_phase}")
        is_running_writing_has_begun_1 = True
        # Display scary text to scare writer
        disappearing_text_label.place(x=610, y=200)
        disappearing_text_label.config(text="YOUR NIGHTMARE BEGINS!")
        keep_writing_label.place(x=610, y=330)
        keep_writing_label.config(text="START WRITING NOW & DONT EVER STOP!")
        regret_label.config(text="OR ELSE!!!")
        regret_label.place(x=900, y=370)

        count_down(4,0)
        writing_phase += 1
        if writing_phase == 2:
            window.after(4000, writing_has_begun_2)
    else:
        is_running_writing_has_begun_1 = False
        return is_running_writing_has_begun_1

#writing_phase = 2
def writing_has_begun_2():
    global writing_phase, writing_stopped, writing_time_limit,is_running_writing_has_begun_2
    global count, counter, time_out

    if not writing_stopped and not is_running_writing_has_begun_2:
        keyboard_not_pressed = False
        is_running_writing_has_begun_2 = True
        print(f"2 writing_phase: {writing_phase}")
        # Display textbox afterwards and wipe scary messages
        disappearing_text_label.config(text="")
        keep_writing_label.config(text="")
        regret_label.config(text="")

        writing_text.place(x=638, y=300)

        print(f"2/ writing_phase: {writing_phase}")
        # Check for timeout when user stops typing - JUST COMPARE TEMPORARY TEXT TO TEXT IN TEXTBOX
        # How to check for user input?

        writing_time_limit = 15 * 60
        count_down(writing_time_limit,writing_time_limit)
        window.after(1000, check_for_AFK)
        print(f"count: {count}")
        print(f"2/ counter: {counter}")
        # How to listen to all keys on keyboard
        # if wait_for_user(2)==False: #Keyboard input check is ignored. Why?

        window.after(1000, check_for_proceed)
        # canvas.itemconfig(writing_text, text="abc")
        # canvas.delete()
    else:
        is_running_writing_has_begun_2 = False
        return is_running_writing_has_begun_2

# START TIMER ONLY WHEN USER IS NOT TYPING ANYTHING
# AFTER TIMEOUT SHOW SCARY MESSAGES
def writing_time_out():
    global writing_phase, time_out, writing_stopped
    writing_text.place_forget()  # can also wipe all text depending on feature
    disappearing_text_label.place(x=610, y=200)
    disappearing_text_label.config(text="DELETED!!! YOUR NIGHTMARE CONTINUES!!!!!")
    keep_writing_label.config(text="Is regret starting to seep into your veins?")
    keep_writing_label.place(x=630, y=300)
    regret_label.config(text="SUCH A WASTE OF EFFORT... ...", font=(FONT_NAME, 30))
    regret_label.place(x=610, y=370)

    stop_button.place_forget()
    start_button.place(x=900, y=450)
    start_button.config(text="I beg u! Let me continue please!")
    writing_phase = 2 #redirect back to writing mode/phase
    writing_stopped = True
    time_out = True


# Button to stop writing (And save progress?)
# How to stop running program or stop all function calls?
# Reset whole layout + try to stop all running functions
def writing_has_ceased():
    global writing_stopped
    #ADD A GLOBAL VARIABLE TO ACT AS A SWITCH & CHANGE ITS STATE ACCORDINGLY, THEN RETURN ANY VALUE IN THOSE FUNCTIONS ITSELF
    # Try to stop all running functions #Tkinter how to stop event loop ---> JUST RETURN ANY VALUE
    # window.after_cancel(writing_has_begun_0)
    # window.after_cancel(writing_has_begun_1)
    # window.after_cancel(writing_has_begun_2)
    writing_stopped = True
    # Try to get text and store in text file?
    # print(writing_text.get())
    reset()


def reset():
    # Reset whole layout, timers, texts,
    global writing_stopped, start_button, stop_button, disappearing_text_label, keep_writing_label, regret_label, writing_phase, timer_text, count, writing_time_limit

    writing_text.place_forget()
    stop_button.place_forget()
    disappearing_text_label = Label(text="Be warned!", fg=BLOOD_RED, bg=DARK_RED,
                                    font=(FONT_NAME, 35))
    keep_writing_label = Label(text="Keep writing or you will                                               it!!",
                               fg=PINK,
                               bg=DARK_RED,
                               font=(FONT_NAME, 16))
    regret_label = Label(text="REGRET", fg=BLOOD_RED, bg=DARK_RED,
                         font=(SCARY_FONT, 55, "bold"))
    disappearing_text_label.place(x=610, y=300)
    keep_writing_label.place(x=610, y=400)
    regret_label.place(x=900, y=370)
    canvas.itemconfig(timer_text, text="00:00")

    start_button = Button(text="PLEASE LET ME START WRITING MY SPECIAL NOVEL...", fg="white", bg=PINK,
                          font=(FONT_NAME, 15),
                          highlightthickness=0, command=writing_has_begun_0)
    start_button.place(x=725, y=445)
    writing_phase = 0
    count = 0
    writing_time_limit=5


def delete_text():
    writing_text.delete(1.0, END)
    writing_text.insert(END, "")


def check_for_AFK(): #in writing_has_begun_2
    # If writer is AFK, delete all text that has been written
    # RECURSIVE
    global time_out, counter, count, compare_text
    if not time_out:
        # Checks every second for user text VS compare_text
        if compare_text == writing_text.get(1.0, END):
            if counter == 10:
                window.after(1000, delete_text)
                counter = -1
                print(f"counter:{counter}")
            # Calls itself & Checks every second
            window.after(1000, check_for_AFK)
            counter += 1
            print(f"counter:{counter}")
        else:
            # IF WRITER NOT AFK, GET NEW TEXT, CALL ITSELF
            window.after(1000, check_for_AFK)
            compare_text = writing_text.get(1.0, END)
            counter = 0


def check_for_proceed(): #in writing_has_begun_2
    # Check whether to proceed to show "all text deleted" notification
    global writing_phase, time_out
    global counter, count
    print("check_for_proceed()")
    if not time_out and not writing_stopped:
        count = 5
        print(f"count:{count}")
        print(f"counter:{counter}")

        if writing_phase == 2 and counter == 5:
            count_down(count,0)
            print(f"check_for_proceed; count= {count}")
            window.after(1000, writing_time_out)
            writing_phase = 0
        else:
            window.after(1000, check_for_proceed)
    else:
        return 0

        # DONT KNOW HOW TO DISPLAY COUNTDOWN TIMER BEFORE TEXTCLEAR PROPERLY
        # OH... JUST DISPLAY COUNTER AS timer_text... but it might not countdown...
        # Once AFK counter hits 3; will proc "deleted text message",
        # cannot queue check_for_AFK counter vs check_for_proceed countdown timer display




# Countdown mechanism
def count_down(count,writing_time):
    global timer_text, writing_stopped, countdown_switch
    if not writing_stopped or not countdown_switch:
        countdown_switch = True
        count_min = math.floor(count / 60)
        count_sec = count % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"

        canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
        if count > 0:
            global timer
            writing_time-=1
            timer = window.after(1000, count_down, count - 1,writing_time)

        if count == 0:
            canvas.itemconfig(timer_text, text="")
    else:
        countdown_switch = False
        return countdown_switch

# --------------UI/WINDOW-----------------------#
window = Tk()
window.title("Disappearing Text")
window.config(padx=0, pady=0)  # bg=DARK_RED)
window.minsize(width=1920, height=1080)

canvas = Canvas(width=1920, height=1080, bg=DARK_RED, highlightthickness=0)
scary_thought_bubble = PhotoImage(file="ScaryThoughtBubble.png")
canvas.create_image(1920 / 2, 1080 / 2, image=scary_thought_bubble)
canvas.place(x=0, y=0)

# --------------LABELS-----------------------#
disappearing_text_label = Label(text="Be warned!", fg=BLOOD_RED, bg=DARK_RED,
                                font=(FONT_NAME, 35))
keep_writing_label = Label(text="Keep writing or you will                                               it!!", fg=PINK,
                           bg=DARK_RED,
                           font=(FONT_NAME, 16))
regret_label = Label(text="REGRET", fg=BLOOD_RED, bg=DARK_RED,
                     font=(FONT_NAME, 55, "bold"))

# Tkinter limitation? Cant change Entry Label background color (Use text instead)
writing_text = Text(window, height=6, width=45, bg=DARK_RED, fg=BLOOD_RED, highlightthickness=0, font=(FONT_NAME, 15))
writing_text.focus()
# writing_text = Entry(width=1000)
# Create text on canvas--> click button to allow edits? But dont want the ugly white textbox background
# writing_text = canvas.create_text(100, 200, text="", fill=BLOOD_RED, font=(FONT_NAME,10, "bold"))

start_button = Button(text="PLEASE LET ME START WRITING MY SPECIAL NOVEL...", fg="white", bg=PINK, font=(FONT_NAME, 15),
                      highlightthickness=0, command=writing_has_begun_0)
stop_button = Button(text="I BETTER STOP WRITING NOW...", fg="white", bg=PINK, font=(FONT_NAME, 15),
                     highlightthickness=0, command=writing_has_ceased)

# --------------------------------------------#
disappearing_text_label.place(x=610, y=300)
keep_writing_label.place(x=610, y=400)
regret_label.place(x=900, y=370)
start_button.place(x=725, y=445)
timer_text = canvas.create_text(950, 100, text="00:00", fill=BLOOD_RED, font=(FONT_NAME, 60, "bold"))

window.mainloop()
# --------------------------------------------#
