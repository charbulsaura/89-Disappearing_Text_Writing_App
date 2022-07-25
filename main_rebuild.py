from tkinter import *
import pyglet, os
from pyglet import font
import math
import time
import keyboard

FONT_NAME = "Lucida Handwriting"
SCARY_FONT = font.add_file('Creepster_Regular.ttf')
PINK = "#ed594e"
BLOOD_RED = "#ff3838"
DARK_RED = "#5e1212"
BLACK = "#030202"

compare_text = ""
count = 15 * 60
counter = 0
writing_phase = 0
# writing_time_limit = 15*60

# Tkinter widgets stacking on each other
# Tkinter widgets multiple instances on button click

# FUNCTION CONTROL OBJECTS
timer = None
timer_1 = None
check_for_afk_object = None
check_for_afk_object2 = None
writing_time_out_object = None
writing_1_object = None
writing_2_object = None

# STILL NEED TO FIX MULTIPLE FUNCTION INSTANCES!!! TKINTER LIMITATION
# >> CREATE OBJECTS FOR ALL FUNCTION RUNS SO IT CAN BE CONTROLLED BY window.after_cancel
# TO PREVENT PARALLEL FUNCTION RUNS, CREATE ANOTHER SWITCH TO TAKE NOTE IF FUNCTION IS RUNNING OR NOT.
# >> Switch doesnt work bcos it just continues running from previous state once restarted
# >> Switch works. just have to place in correct place & separate from function call itself
# TO FLIP SWITCH, FUNCTION RETURNS VALUE TO CHANGE STATE OF SWITCH
time_out = False
writing_stopped = False
check_for_proceed_countdown_timer = False
# Trying solution: Implement switch for every function + window.after_cancel object
stop_writing_has_begun_0 = False
stop_writing_has_begun_1 = False
stop_writing_has_begun_2 = False
stop_writing_time_out = False
stop_countdown = False
stop_check_for_AFK = False
stop_check_for_proceed = False


def start_btn():
    # START BUTTON
    # >>Seperated into different functions to prevent instant function calls
    global stop_writing_has_begun_0, stop_writing_has_begun_1, stop_writing_has_begun_2, \
        stop_writing_time_out, stop_countdown, stop_check_for_AFK, stop_check_for_proceed
    global writing_phase, writing_stopped, count, time_out
    global stop_writing_has_begun_0, stop_writing_has_begun_1, stop_writing_has_begun_2
    global timer, timer_1, check_for_afk_object, check_for_afk_object2, writing_time_out_object, writing_1_object, writing_2_object
    # Turn off all function switch
    print("START BUTTON PRESSED: CHECKING FUNCTION SWITCHES")
    stop_writing_has_begun_0 = False
    print(f"stop_writing_has_begun_0:{stop_writing_has_begun_0}")
    stop_writing_has_begun_1 = False
    print(f"stop_writing_has_begun_1:{stop_writing_has_begun_1}")
    stop_writing_has_begun_2 = False
    print(f"stop_writing_has_begun_2:{stop_writing_has_begun_2}")
    stop_writing_time_out = False
    print(f"stop_writing_time_out:{stop_writing_time_out}")
    stop_countdown = False
    print(f"stop_countdown:{stop_countdown}")
    stop_check_for_AFK = False
    print(f"stop_check_for_AFK:{stop_check_for_AFK}")
    stop_check_for_proceed = False
    print(f"stop_check_for_proceed:{stop_check_for_proceed}\n")

    # Flip the switch to allow all functions to continue running.
    # But why does the function calls continue from before instead of new state?
    # Seems like a new instance is being created every time the button is clicked...
    writing_stopped = False
    time_out = False
    start_button.place_forget()
    stop_button.place(x=1000, y=650)

    # ALSO RESET ALL OBJECTS --- TO STOP FUNCTION RUN
    timer = None
    timer_1 = None
    check_for_afk_object = None
    check_for_afk_object2 = None
    writing_time_out_object = None
    writing_1_object = None
    writing_2_object = None

    # ------------TEXT INPUT----------------------#
    # Implement appearing text on screen at different intervals
    disappearing_text_label.config(text="")
    keep_writing_label.config(text="")
    regret_label.config(text="")

    writing_has_begun_0()


def reset():
    # Reset whole layout, timers, texts,
    global writing_stopped, start_button, stop_button, disappearing_text_label, keep_writing_label, \
        regret_label, writing_phase, timer_text, count, writing_time_limit, timer, timer_1, writing_1_object, writing_2_object
    global stop_writing_has_begun_0, stop_writing_has_begun_1, stop_writing_has_begun_2, \
        stop_writing_time_out, stop_countdown, stop_check_for_AFK, stop_check_for_proceed
    global check_for_afk_object, writing_time_out_object, writing_1_object
    # Turn on all function switch
    print("STOP BUTTON PRESSED: CHECKING FUNCTION SWITCHES")
    stop_writing_has_begun_0 = True
    print(f"stop_writing_has_begun_0:{stop_writing_has_begun_0}")
    stop_writing_has_begun_1 = True
    print(f"stop_writing_has_begun_1:{stop_writing_has_begun_1}")
    stop_writing_has_begun_2 = True
    print(f"stop_writing_has_begun_2:{stop_writing_has_begun_2}")
    stop_writing_time_out = True
    print(f"stop_writing_time_out:{stop_writing_time_out}")
    stop_countdown = True
    print(f"stop_countdown:{stop_countdown}")
    stop_check_for_AFK = True
    print(f"stop_check_for_AFK:{stop_check_for_AFK}")
    stop_check_for_proceed = True
    print(f"stop_check_for_proceed:{stop_check_for_proceed}\n")

    try:
        window.after_cancel(timer)
        window.after_cancel(timer_1)
        window.after_cancel(check_for_afk_object)
        window.after_cancel(check_for_afk_object2)
        window.after_cancel(writing_time_out_object)
        window.after_cancel(writing_1_object)
        window.after_cancel(writing_2_object)
        print("RESET timer,timer_1,check_for_afk_object,writing_time_out_object,writing_1_object,writing_2_object")
    except ValueError:
        print("Some objects not found")

    canvas.itemconfig(timer_text, text="00:00")

    # Hide text box & stop button
    writing_text.place_forget()
    stop_button.place_forget()

    # Show start button
    start_button = Button(text="PLEASE LET ME START WRITING MY SPECIAL NOVEL...", fg="white", bg=PINK,
                          font=(FONT_NAME, 15),
                          highlightthickness=0, command=start_btn)

    # Reset all labels-- but why are there still duplicate labels lingering in diff layers???
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
    start_button.place(x=725, y=445)

    writing_phase = 0
    # writing_time_limit = 5 * 60
    # count = 5*60


# Button to stop writing (And save progress?)
# How to stop running program or stop all function calls?
# Reset whole layout + try to stop all running functions
def writing_has_ceased():
    global writing_stopped
    # ADD A GLOBAL VARIABLE TO ACT AS A SWITCH & CHANGE ITS STATE ACCORDINGLY, THEN RETURN ANY VALUE IN THOSE FUNCTIONS ITSELF
    print("STOP BUTTON PRESSED")
    writing_stopped = True
    reset()


def delete_text():
    writing_text.delete(1.0, END)
    writing_text.insert(END, "")


def writing_has_begun_0():
    global writing_phase, writing_stopped, count, time_out
    global stop_writing_has_begun_0, stop_writing_has_begun_1, stop_writing_has_begun_2
    global timer, timer_1, check_for_afk_object, writing_time_out_object, writing_1_object, writing_2_object

    # Countdown and show starting text before user begins writing
    print("0.writing_has_begun")
    if not stop_writing_has_begun_0:
        if writing_phase == 0:
            count_down_message(2)
            writing_phase += 1
        if writing_phase == 1:
            writing_1_object = window.after(2000, writing_has_begun_1)
            stop_writing_has_begun_1 = False
        elif writing_phase == 2:
            writing_2_object = window.after(2000, writing_has_begun_2)
            stop_writing_has_begun_2 = False
        stop_writing_has_begun_0 = True
        # stop_writing_has_begun_1 = False


# writing_phase = 1
def writing_has_begun_1():  # writing_1_object
    global writing_phase, writing_stopped, stop_writing_has_begun_0, stop_writing_has_begun_1, stop_writing_has_begun_2
    print(f"stop_writing_has_begun_1: {stop_writing_has_begun_1}")
    if not stop_writing_has_begun_1:
        # Stop previous function
        stop_writing_has_begun_0 = True
        print("1.DISPLAYING SCARY TEXT")
        # Display scary text to scare writer
        disappearing_text_label.place(x=610, y=200)
        disappearing_text_label.config(text="YOUR NIGHTMARE BEGINS!")
        keep_writing_label.place(x=610, y=330)
        keep_writing_label.config(text="START WRITING NOW & DONT EVER STOP!")
        regret_label.config(text="OR ELSE!!!")
        regret_label.place(x=900, y=370)

        count_down_message(2)
        writing_phase += 1
        if writing_phase == 2:
            window.after(2000, writing_has_begun_2)
        stop_writing_has_begun_1 = True
        stop_writing_has_begun_2 = False
    print(f"stop_writing_has_begun_1: {stop_writing_has_begun_1}")


# writing_phase = 2
def writing_has_begun_2():  # writing_2_object
    global writing_phase, writing_stopped, stop_writing_has_begun_1
    global count, counter, time_out, writing_time_out_object, check_for_afk_object
    print(f"stop_writing_has_begun_2: {stop_writing_has_begun_2}")
    if not stop_writing_has_begun_2:
        # Stop previous function
        stop_writing_has_begun_1 = True
        print(f"2.count: {count}")
        # Display textbox afterwards and wipe scary messages
        disappearing_text_label.config(text="")
        keep_writing_label.config(text="")
        regret_label.config(text="")

        print("2.TEXTBOX CREATED")
        writing_text.place(x=638, y=300)

        # Check for timeout when user stops typing - JUST COMPARE TEMPORARY TEXT TO TEXT IN TEXTBOX
        # How to check for user input?
        # How to listen to all keys on keyboard

        # writing_time_limit = 15 * 60
        count_down()
        print("2.TIMER CREATED")
        print(f"count: {count}")
        check_for_afk_object = window.after(1000, check_for_AFK)
        writing_time_out_object = window.after(1000, check_for_proceed)
    print(f"stop_writing_has_begun_2: {stop_writing_has_begun_2}")


# START TIMER ONLY WHEN USER IS NOT TYPING ANYTHING
# AFTER TIMEOUT SHOW SCARY MESSAGES
def writing_time_out():
    global writing_phase, time_out, writing_stopped
    global stop_writing_has_begun_0, stop_writing_has_begun_1, stop_writing_has_begun_2, check_for_proceed_countdown_timer

    # Stop all writing phases
    stop_writing_has_begun_0 = True
    stop_writing_has_begun_1 = True
    stop_writing_has_begun_2 = True
    check_for_proceed_countdown_timer = False

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
    writing_phase = 2  # redirect back to writing mode/phase
    # After AFK detected, stop checking
    window.after_cancel(check_for_afk_object)
    window.after_cancel(timer)
    writing_stopped = True
    time_out = True


# in writing_has_begun_2
def check_for_AFK():  # check_for_afk_object
    # If writer is AFK, delete all text that has been written
    # RECURSIVE
    global time_out, counter, count, compare_text, check_for_afk_object, check_for_afk_object2
    print("check_for_AFK()")
    # Checks every second for user text VS compare_text
    if compare_text == writing_text.get(1.0, END):
        if counter == 10:  # Delete text once counter reaches 10 s #test with 5 sec
            window.after(1000, delete_text)
            counter = -1
            print(f"counter:{counter}")
        # Calls itself & Checks every second
        check_for_afk_object2 = window.after(1000, check_for_AFK)
        counter += 1
        print(f"counter:{counter}")
    else:
        # IF WRITER NOT AFK, GET NEW TEXT, CALL ITSELF
        check_for_afk_object2 = window.after(1000, check_for_AFK)
        compare_text = writing_text.get(1.0, END)
        counter = 0

def timer_before_deleting():
    global counter
    count_down_message(counter)

# in writing_has_begun_2
def check_for_proceed():  # writing_time_out_object
    # Want to show countdown at same timing when checking for AFK
    # Check whether to proceed to show "all text deleted" notification
    global writing_phase, time_out, writing_time_out_object
    global counter, count, check_for_proceed_countdown_timer
    print("check_for_proceed()")
    check_for_proceed_countdown_timer = True
    timer_before_deleting()
    if writing_phase == 2 and counter == 10:
        window.after(1000, writing_time_out)
        writing_phase = 0
    else:
        window.after_cancel(writing_time_out_object)
        window.after(1000, check_for_proceed)


# Countdown mechanism: Implement 2- separate for writing time limit and other for message
# FINALLY FIXED with 2 counters; if not it gets messy
def count_down_message(count1):  # timer_1 object
    global timer_1, check_for_proceed_countdown_timer, counter
    count_min = math.floor(count1 / 60)
    count_sec = count1 % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if check_for_proceed_countdown_timer == True:
        if counter >10:
            canvas.itemconfig(timer_text_2, text=f"PLEASE WRITE SOMETHING! TIME REMAINING BEFORE DELETION= 00:{10-counter}",font=(FONT_NAME, 20, "bold"))
        else:
            canvas.itemconfig(timer_text_2, text=f"PLEASE WRITE SOMETHING! TIME REMAINING BEFORE DELETION= 00:0{10-counter}",font=(FONT_NAME, 20, "bold"))
    else:
        canvas.itemconfig(timer_text_2, text=f"{count_min}:{count_sec}")
    if count1 > 0:
        global timer_1
        timer_1 = window.after(1000, count_down_message, count1 - 1, )

    if count1 == 0:
        canvas.itemconfig(timer_text_2, text="")
        window.after_cancel(timer_1)

def count_down():  # timer object
    global timer, timer_text, count, writing_stopped
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    print(f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        count = count - 1
        timer = window.after(1000, count_down)

    if count == 0:
        canvas.itemconfig(timer_text, text="why 0 and not 14.xx???")  # bcos u reset global var when stop button pressed


# --------------UI/WINDOW-----------------------#
window = Tk()
window.title("Disappearing Text")
window.config(padx=0, pady=0)
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

writing_text = Text(window, height=6, width=45, bg=DARK_RED, fg=BLOOD_RED, highlightthickness=0, font=(FONT_NAME, 15))
writing_text.focus()

start_button = Button(text="PLEASE LET ME START WRITING MY SPECIAL NOVEL...", fg="white", bg=PINK, font=(FONT_NAME, 15),
                      highlightthickness=0, command=start_btn)
stop_button = Button(text="I BETTER STOP WRITING NOW...", fg="white", bg=PINK, font=(FONT_NAME, 15),
                     highlightthickness=0, command=writing_has_ceased)

# --------------------------------------------#
disappearing_text_label.place(x=610, y=300)
keep_writing_label.place(x=610, y=400)
regret_label.place(x=900, y=370)
start_button.place(x=725, y=445)
timer_text_2 = canvas.create_text(950, 50, text="", fill="white", font=(FONT_NAME, 40, "bold"))
timer_text = canvas.create_text(950, 100, text="", fill=BLOOD_RED, font=(FONT_NAME, 60, "bold"))

window.mainloop()
# --------------------------------------------#
