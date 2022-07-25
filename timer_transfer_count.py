from tkinter import *
import time
import math

# Allows timer to continue from where it left off
writing_time = 15 * 60
count = 15 * 60
timer = None
timer_label_item = None

stop_running_functions = False


# def transfer_time():
#     count_down()
#     window.after(1000, transfer_time)


def timer_label():
    global count
    # timer_text_unformatted = Label(text=f"{writing_time}", fg="black", bg="green")
    timer_text_unformatted = Label(text=f"{count}", fg="black", bg="green")
    timer_text_unformatted.place(x=100, y=200)

# IF U SPAM CLICK START BUTTON IT WILL COUNTDOWN SUPER FAST...
# THATS WHATS CAUSING THE GLITCHY BEHAVIOUR IN UR MAIN PROGRAM
# How to prevent/stop multiple instances of tkinter widget from occurring?
# (Cant stop, but can stop all at once with button...)
def start():
    global stop_running_functions
    stop_running_functions = False
    count_down()

def stop():
    global stop_running_functions
    # Testing how to stop function calls
    window.after_cancel(timer)  # but this stops timer altogether
    window.after_cancel(timer_label_item)  # only stops 1 instance/ 1 frame or 1 second
    print(f"stop_running_functions: {stop_running_functions}")
    stop_running_functions = True
    print(f"stop_running_functions: {stop_running_functions}")


def count_down():
    global count, timer, timer_label_item, stop_running_functions
    if not stop_running_functions:
        # timer_label_item = window.after(1000,timer_label)
        print("still running, stop_running_function didnt proc")
        count_min = math.floor(count / 60)
        count_sec = count % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
        print(f"{count_min}:{count_sec}")
        if count > 0:
            timer_label_item = window.after(1000, timer_label)
            count = count - 1
            timer = window.after(1000, count_down)

        if count == 0:
            print("00:00")



# def count_down(count):
#     global writing_time
#     count_min = math.floor(count / 60)
#     count_sec = count % 60
#     if count_sec < 10:
#         count_sec = f"0{count_sec}"
#     canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
#     print(f"{count_min}:{count_sec}")
#     if count > 0:
#         writing_time -= 1
#         timer_text_unformatted.config(text=f"{writing_time}")
#         print(f"writing_time: {writing_time}")
#         window.after(1000, count_down, count - 1,)
#
#     if count == 0:
#         print("00:00")

# -----------------------------------------------------------------#

window = Tk()
window.title("Timer Test")
window.config(padx=0, pady=0)
window.minsize(width=500, height=500)

canvas = Canvas(width=1920, height=1080, bg="black", highlightthickness=0)
canvas.place(x=0, y=0)

Start = Button(text="Start timer test", fg="black", bg="green", command=start)
# Button_1 = Button(text="Start timer test", fg="black", bg="green", command=transfer_time)
Start.place(x=300, y=200)
Stop = Button(text="Stop timer test", fg="black", bg="green", command=stop)
Stop.place(x=400, y=200)

timer_text = canvas.create_text(200, 210, text="", fill="green")

window.mainloop()
