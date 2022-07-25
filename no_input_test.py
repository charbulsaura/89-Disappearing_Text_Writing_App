import keyboard
def wait_for_user(secs):
    import msvcrt
    import time
    start = time.time()
    while True:
        if msvcrt.kbhit():
            msvcrt.getch()
            print("input detected")
            break
        if time.time() - start > secs:
            print("no input")
            break

wait_for_user(2)