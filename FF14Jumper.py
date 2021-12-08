import threading
import win32gui
import win32con
import datetime
import sys
import time


def find_window(title):
    """find a window by title"""
    return win32gui.FindWindow(None, title)


def mouse_click(hw):
    """click"""
    hw.SetForegroundWindow()    # bring to front
    hw.SetActiveWindow()        # set as active
    hw.SetFocus()               # set as focus
    send_key(hw, win32con.MK_LBUTTON)           # left click


def send_key(hw, key):
    """send key"""
    win32gui.SendMessage(hw, win32con.WM_KEYDOWN, key, 0)
    time.sleep(0.5)
    win32gui.SendMessage(hw, win32con.WM_KEYUP, key, 0)


def log(text):
    """log"""
    print('[{now}] - {text}'.format(now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), text=text))


def jump(hw):
    """jump"""
    log("Jumping...")
    win32gui.SetForegroundWindow(hw)   # bring to front
    win32gui.SetActiveWindow(hw)       # set as active
    send_key(hw, 0x57)                 # W
    send_key(hw, 0x53)                 # S
    send_key(hw, win32con.VK_SPACE)
    log("Jumped!")


def loop_jump(hw, minute, kill_event):
    """loop jump"""
    interval = 60 * minute
    while not kill_event.wait(1):
        t = threading.Thread(target=jump, args=(hw,))
        t.start()
        t.join()
        log("Sleep for {interval} seconds...".format(interval=interval))
        time.sleep(interval)


def main():
    ff14_class_name = "FINAL FANTASY XIV"

    hw = find_window(ff14_class_name)

    if(hw == 0):
        print("FFXIV Window not found")
        exit(1)

    sleepMinute = 2
    if(len(sys.argv) > 1 and sys.argv[1].isdigit()):
        sleepMinute = int(sys.argv[1])
        print("Sleep for {sleepMinute} minutes".format(
            sleepMinute=sleepMinute))
    else:
        print("Sleep for default {sleepMinute} minutes".format(
            sleepMinute=sleepMinute))

    print("Press enter to stop")

    kill_event = threading.Event()
    t = threading.Thread(target=loop_jump, args=(hw, sleepMinute, kill_event))
    t.start()

    if(input() is not None):
        kill_event.set()
        log("Stopping...")
        t.join()

    exit(0)


if __name__ == "__main__":
    main()
