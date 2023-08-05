import pyautogui
import time
import os
import sys


def cls(bootleg=False):
    """
    Commented out - bootleg "clear console" for Pycharm,
    use while writing, and switch to "os.system..." line when
    packing into .exe

    for getting coordinates:
    time.sleep(2)
    print(pyautogui.position())

    launch program, and move cursor to the simulated console window,
    after 2s you'll get coordinates to put as pyautogui.click() arguments
    :return:
    """

    if bootleg:
        time.sleep(0.1)
        pyautogui.click(x=778, y=832)
        pyautogui.hotkey('ctrl', 'l')
    else:
        os.system('cls' if os.name == 'nt' else 'clear')


def get_script_location():
    """
    :return: directory of python script executing it
    """
    return os.path.dirname(os.path.realpath(sys.argv[0]))
