import pytesseract
import subprocess
import pyautogui
from PIL import ImageGrab
import time
import random  # Import random module for generating random durations
import pygetwindow as gw
import keyboard

# Set the Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

def capture_and_recognize(x1, y1, x2, y2, time_interval=0.5):
    """Capture a screen region and recognize text using OCR."""
    time.sleep(time_interval)  # Wait for the specified interval
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))  # Capture the screen region
    text = pytesseract.image_to_string(screenshot, config='--psm 6 digits')  # Perform OCR
    print("Screenshot text:", text)  # Output the recognized text
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
    try:
        while True:
            # Check for Ctrl+C key press
            if keyboard.is_pressed('ctrl+c'):
                print("Ctrl+C detected. Exiting...")
                break

            # Move to the specified position
            pyautogui.moveTo(x, y, duration=2)

            # Check if the active window is "MapleStory"
            active_window = gw.getActiveWindow()
            if not active_window or "MapleStory" not in active_window.title:
                print("Active window is not MapleStory. Exiting...")
                break

            # Press and hold the left arrow key for a random duration between 1 to 3 seconds
            pyautogui.keyDown('left')
            time.sleep(random.uniform(1, 3))
            pyautogui.keyUp('left')

            # Click 4 times with a 0.2-second interval
            for _ in range(4):
                pyautogui.click(x, y)
                time.sleep(0.2)

            # Press and hold the right arrow key for a random duration between 1 to 3 seconds
            pyautogui.keyDown('right')
            time.sleep(random.uniform(1, 3))
            pyautogui.keyUp('right')

            # Click 4 times with a 0.2-second interval
            for _ in range(4):
                pyautogui.click(x, y)
                time.sleep(0.2)

    except KeyboardInterrupt:
        print("Process interrupted by user. Exiting...")
