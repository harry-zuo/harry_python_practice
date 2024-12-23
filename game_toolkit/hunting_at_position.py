import pyautogui
from util import hunting_at_position  # Import necessary functions

if __name__ == "__main__":
    # Enable pyautogui's fail-safe feature to prevent accidental movements
    pyautogui.FAILSAFE = True
    
    x, y = 621, 305  # Define initial coordinates
    pyautogui.moveTo(x, y, duration=2)  # Move to initial position

    hunting_at_position(x, y)  # Click at the specified position 
