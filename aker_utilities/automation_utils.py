import pyautogui
import time


def keep_mouse_busy() -> None:
    """
    Draw rectangle with mouse pointer to keep pc awake and responsive.
    """
    while True:
        pyautogui.FAILSAFE = False
        pyautogui.moveRel(0, 50)
        time.sleep(2)
        pyautogui.moveRel(-50, 0)
        time.sleep(2)
        pyautogui.moveRel(0, -50)
        time.sleep(2)
        pyautogui.moveRel(50, 0)
        time.sleep(2)
