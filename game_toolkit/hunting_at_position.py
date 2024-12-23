import pyautogui
from util import hunting_at_position  # Import necessary functions

if __name__ == "__main__":
    # Enable pyautogui's fail-safe feature to prevent accidental movements
    pyautogui.FAILSAFE = True
    
    # x, y = 644, 308  # Define initial coordinates
    x, y = 770, 423  # Define initial coordinates
    pyautogui.moveTo(x, y, duration=2)  # Move to initial position

    close_window_config = 12, 37, 380, 333
    hunting_at_position(x, y, close_window_config)  # Click at the specified position 
