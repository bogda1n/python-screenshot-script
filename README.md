# 📸 Screenshot Tool with OCR | Python

A **cross-platform** (macOS & Windows) Python-based **screenshot tool** that allows you to:  

✅ **Select custom screen areas** for screenshots and OCR (like Windows Snipping Tool)  
✅ **Take multiple screenshots** with a single key press (**Page Up**)  
✅ **Extract text** from a specific area using **OCR** (powered by EasyOCR)  
✅ **Auto-name screenshots** based on extracted text or timestamp  
✅ **Save screenshots** directly to a local folder  
✅ **Exit anytime** using **Esc**  

---

## 🚀 Features

- **Custom Area Selection**: Select the **screenshot** and **OCR** areas at the start.  
- **Hotkey Trigger**: Use **Page Up** to capture screenshots without re-selecting areas.  
- **OCR Integration**: Extract text from any part of the screen and auto-name files.  
- **Cross-Platform**: Works on both **macOS** and **Windows**.  
- **Simple & Efficient**: No fancy UI—just the essentials for speed and clarity.  

---

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bogda1n/screenshot-tool.git
   cd screenshot-tool

2. **Install dependencies**:
   ```bash
   pip install pyautogui easyocr pillow numpy keyboard
3. **For Linux users (tkinter install):**
   ```bash
   sudo apt-get install python3-tk
---

## 🎯 Usage

1.	**Run the tool**:
 ```bash
    python3 screenshot_tool.py
```
2.	**Select Areas**:
	  -	First, select the screenshot area.
	  -	Then, select the OCR area (to read text for file names).
3.	**Controls**:
	  -	Page Up → Take a screenshot
    -	Esc → Exit the tool
4.	Screenshots saved in: /screenshots folder (auto-created if missing).

---

## 📂 Folder Structure

```
screenshot-tool/
│
├── screenshot_tool.py       # Main Python script
├── screenshots/             # Saved screenshots
└── requirements.txt         # List of dependencies
```
---

## ⚡ To-Do
-	Add support for multi-monitor setups
-	Implement sound/visual alerts after capture
-	Add customizable hotkeys via config file

## ⭐ Star this repo if you find it helpful and feel free to submit issues or PRs! 🚀
