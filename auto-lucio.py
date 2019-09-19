#I saw in the gameplays that professionals Lucio's player switch the speed boost and healing every F**KING second, so I made a simple script that do this
# This script press the shift button every 0.2s
import pyautogui
import time

while (1):
    time.sleep(0.2)
    pyautogui.press('shift')
    
