import pyautogui
import keyboard
import os
import easyocr
from datetime import datetime
import re
import numpy as np
from PIL import Image

# --------- CONFIG ---------
SAVE_FOLDER = "screenshots"  # Folder to save screenshots
TRIGGER_KEY = "page up"           # Trigger Key to take a screenshot
EXIT_KEY = "esc"             # Press Esc to exit

# Define the region to capture (left, top, width, height)
SCREEN_REGION = (100, 200, 800, 600)
# ----------------------------------

# Create folder if it doesn't exist
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Initialize OCR reader (English language)
ocr_reader = easyocr.Reader(['en'], gpu=True) 

def sanitize_filename(text):
    """Removes invalid characters from filename."""
    return re.sub(r'[\\/*?:"<>|]', '', text).strip()

print(f"Press '{TRIGGER_KEY}' to take a screenshot.")
print(f"Press '{EXIT_KEY}' to exit.")

screenshot_count = 0

while True:
    try:
        if keyboard.is_pressed(TRIGGER_KEY):
            # Take screenshot of specific region
            screenshot = pyautogui.screenshot(region=SCREEN_REGION)

            # Convert screenshot to numpy array for easyocr
            screenshot_array = np.array(screenshot)

            # Run OCR to extract text
            result = ocr_reader.readtext(screenshot_array)

            # Get the most confident text or fallback to timestamp
            extracted_text = result[0][1] if result else ''
            clean_text = sanitize_filename(extracted_text)

            if clean_text:
                filename = f"{clean_text}.png"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"

            filepath = os.path.join(SAVE_FOLDER, filename)
            screenshot.save(filepath)

            screenshot_count += 1
            print(f"[{screenshot_count}] Screenshot saved as: {filename}")

            # Prevent multiple captures on single keypress
            while keyboard.is_pressed(TRIGGER_KEY):
                pass

        if keyboard.is_pressed(EXIT_KEY):
            print("Exiting screenshot tool.")
            break

    except KeyboardInterrupt:
        print("Exited manually.")
        break