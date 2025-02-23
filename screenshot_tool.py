import tkinter as tk
from tkinter import messagebox
import pyautogui
import easyocr
import numpy as np
import os
from datetime import datetime
import re
from PIL import ImageGrab
import keyboard

# --------- CONFIGURATION ---------
SAVE_FOLDER = "screenshots"  # Folder to save screenshots
TRIGGER_KEY = "page up"      # Press Page Up to take a screenshot
EXIT_KEY = "esc"             # Press Esc to exit
# ----------------------------------

# Initialize OCR reader
ocr_reader = easyocr.Reader(['en'], gpu=True)

# Create folder if it doesn't exist
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def sanitize_filename(text):
    """Remove invalid filename characters."""
    return re.sub(r'[\\/*?:"<>|]', '', text).strip()

class SnippingTool:
    def __init__(self):
        self.capture_area = None
        self.ocr_area = None
        self.select_areas()

    def select_areas(self):
        """Handles the UI to select capture and OCR areas."""
        self.selection_stage = "capture"
        self.start_x = None
        self.start_y = None
        self.rect = None

        # Setup Tkinter for selection
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)  # Transparent overlay
        self.root.configure(bg='gray')

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="gray", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        messagebox.showinfo("Snipping Tool", "Select the area to CAPTURE first.")
        self.root.mainloop()

    def on_mouse_down(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_mouse_drag(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_mouse_up(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        selected_area = (int(min(self.start_x, end_x)), int(min(self.start_y, end_y)),
                         int(max(self.start_x, end_x)), int(max(self.start_y, end_y)))

        if self.selection_stage == "capture":
            self.capture_area = selected_area
            messagebox.showinfo("Snipping Tool", "Now, select the area for OCR.")
            self.selection_stage = "ocr"
            self.canvas.delete(self.rect)
        elif self.selection_stage == "ocr":
            self.ocr_area = selected_area
            self.root.destroy()  # Close selection UI
            self.start_key_listener()

    def start_key_listener(self):
        """Listen for key presses to trigger screenshots."""
        print(f"Press '{TRIGGER_KEY.upper()}' to take a screenshot.")
        print(f"Press '{EXIT_KEY.upper()}' to exit.")

        screenshot_count = 0

        while True:
            try:
                if keyboard.is_pressed(TRIGGER_KEY):
                    screenshot_count += 1
                    self.take_screenshot(screenshot_count)
                    # Avoid multiple captures on single keypress
                    while keyboard.is_pressed(TRIGGER_KEY):
                        pass

                if keyboard.is_pressed(EXIT_KEY):
                    print("Exiting screenshot tool.")
                    break

            except KeyboardInterrupt:
                print("Exited manually.")
                break

    def take_screenshot(self, count):
      # Hide Tkinter window before capture
      self.root = tk.Tk()
      self.root.withdraw()

      # Capture screenshot for the selected capture area
      screenshot = ImageGrab.grab(bbox=self.capture_area)

      # OCR on the selected OCR area
      ocr_screenshot = ImageGrab.grab(bbox=self.ocr_area)
      ocr_array = np.array(ocr_screenshot)
      result = ocr_reader.readtext(ocr_array)

      # Extract text or use timestamp
      extracted_text = result[0][1] if result else ''
      clean_text = sanitize_filename(extracted_text)

      if clean_text:
          filename = f"{clean_text}.png"
      else:
          timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
          filename = f"screenshot_{timestamp}.png"

      # Save the screenshot
      filepath = os.path.join(SAVE_FOLDER, filename)
      screenshot.save(filepath)

      print(f"[{count}] Screenshot saved as: {filename}")

      # Destroy the hidden window after capture
      self.root.destroy()

if __name__ == "__main__":
    SnippingTool()
