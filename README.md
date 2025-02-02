# Character Automation
Scripts to automate a character's actions based on specific events in a 2D MMORPG.

# Features
✅ Automated player movement with randomized steps to evade bot detection.
✅ Real-time screen monitoring for target text detection.
✅ Dynamic decision-making based on detected events.
✅ Seamless integration of movement, observation, and action execution.

# How It Works
1. Run PythonApplication1 – Automates player movement using WASD controls with randomized step generation to prevent detection.
2. Run PythonApplicationAlarm – Continuously scans the screen for target text using OCR.
3. If target text is detected, CatchBot executes predefined actions (e.g., attacking, interacting, or responding to the event).
4. If no target is found, PythonApplicationAlarm continues searching for the next target.

# Installation
Ensure you have Python installed, then install the required libraries: pip install pytesseract keyboard opencv-python mss pyautogui numpy

Additional Requirements:
 - Tesseract OCR – Install from here.
 - Ensure tesseract.exe is in your system's PATH.

# Libraries Used
- pytesseract – Extracts text from images using OCR.
- keyboard – Detects key presses and automates inputs.
- mss – Captures screenshots for real-time monitoring.
- opencv-python – Preprocesses images to improve text recognition.
- pyautogui – Simulates keyboard/mouse actions based on detected events.

# Customization
You can modify PythonApplicationAlarm to detect different in-game texts and adjust the actions in CatchBot to suit your needs.

# Future Enhancements
🔹 Add AI-based decision-making for smarter automation.
🔹 Implement configurable hotkeys for manual overrides.
🔹 Optimize performance for lower CPU usage.

# Disclaimer
This project is intended for educational and personal use only. Use it responsibly and ensure compliance with the game's terms of service.
