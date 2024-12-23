import pytesseract
import subprocess
import pyautogui
from PIL import ImageGrab, Image
import time
import datetime
import random  # Import random module for generating random durations
import pygetwindow as gw
import cv2
import numpy as np

# Set the Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

def capture_and_recognize(x1, y1, x2, y2):
    """Capture a screen region and recognize text using OCR."""
    # Capture the screen region
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    # screenshot.save("debug_screenshot.png")
    
    # Convert to OpenCV format
    open_cv_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale
    gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, thresh_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Perform OCR
    custom_config = r'--oem 3 --psm 6 -l eng'
    text = pytesseract.image_to_string(thresh_image, config=custom_config)
    
    return text

def send_notification(title, message):
    """Send a notification on macOS."""
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])  # Execute AppleScript for notification

def play_alert_sound():
    """Play an alert sound."""
    subprocess.run(["afplay", "/System/Library/Sounds/Ping.aiff"])  # Play sound using afplay

def hunting_at_position(x, y):
    """Perform a series of actions involving keyboard and mouse interactions, with interruption handling."""
    pre_exp = ""
    loop_count = 0

    try:
        while True:
            cur_exp = capture_and_recognize(475, 475, 509, 485)
            print(f"current_time: {datetime.datetime.now()} [loop_count: {loop_count}] pre_exp: {pre_exp}, and captured cur_exp: {cur_exp}")
            if not cur_exp:
                print(f"No text captured. Exiting...")
                break
            
            if not pre_exp:
                pre_exp = cur_exp
            
            if loop_count == 10 and pre_exp == cur_exp:
                print(f"Loop count is {loop_count} and pre_exp is same as cur_exp[{cur_exp}]. Exiting...")
                [play_alert_sound() for _ in range(10)]
                break

            # Check if the active window is "MapleStory"
            active_window = gw.getActiveWindow()
            if not active_window or active_window.title() != "Maplestory Worlds Maplestory Worlds":
                print(f"Active window is not 'Maplestory Worlds Maplestory Worlds'. Exiting... {active_window.title()}")
                break

            # Press and hold the left arrow key for a random duration between 1 to 3 seconds
            pyautogui.keyDown('left')
            time.sleep(random.uniform(0.5, 1))
            pyautogui.keyUp('left')

            # Click 4 times with a 0.2-second interval
            for _ in range(6):
                pyautogui.click(x, y)
                time.sleep(0.2)

            # Press and hold the right arrow key for a random duration between 1 to 3 seconds
            pyautogui.keyDown('right')
            time.sleep(random.uniform(0.5, 1))
            pyautogui.keyUp('right')

            # Click 4 times with a 0.2-second interval
            for _ in range(6):
                pyautogui.click(x, y)
                time.sleep(0.2)

            loop_count += 1

    except KeyboardInterrupt:
        print("Process interrupted by user. Exiting...")

if __name__ == "__main__":
    text = capture_and_recognize(475, 475, 509, 485)
    print(f'captured text: {text}')