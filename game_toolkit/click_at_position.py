import pyautogui
from util import capture_and_recognize, play_alert_sound, send_notification

if __name__ == "__main__":
    # Enable pyautogui's fail-safe feature to prevent accidental movements
    pyautogui.FAILSAFE = True
    
    x, y = 556, 233  # Define initial coordinates
    pyautogui.moveTo(x, y, duration=2)  # Move to initial position

    while True:
        text = capture_and_recognize(431, 200, 500, 311)
        
        if any(char in text for char in ['12', '13']):
            for _ in range(3):
                play_alert_sound()
                send_notification("OCR Result", f"Recognized digits: {text}")
            break
