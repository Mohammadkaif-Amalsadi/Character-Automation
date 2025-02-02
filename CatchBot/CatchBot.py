import pyautogui
import time
import pygetwindow as gw
import pytesseract

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def find_target_window():
    # Get all windows
    windows = gw.getWindowsWithTitle("PROClient Monitor")
    
    # Filter out the window with exact title match
    for window in windows:
        if window.title == "PROClient Monitor":
            return window
    return None

def main():
    target_window = find_target_window()
    if not target_window:
        print("PROClient Monitor window not found.")    
        return

    while True:
        x, y, _, _ = target_window.left, target_window.top, target_window.width, target_window.height
        # Get the screen coordinates of the window
        
        # Take a screenshot of the window and read the text
        screenshot = pyautogui.screenshot(region=(x, y, target_window.width, target_window.height))
        text = pytesseract.image_to_string(screenshot)

        if "Target found" in text:
            # Press 1, then ctrl
            time.sleep(2)
            pyautogui.press('1')
            time.sleep(0.2)
            pyautogui.press('3')
            

            # Press 3, then 1
            time.sleep(3)
            pyautogui.press('3')
            time.sleep(0.2)
            pyautogui.press('1') #1

            # Repeat until "Target found" text disappears
            while "Target found" in text:
                screenshot = pyautogui.screenshot(region=(x, y, target_window.width, target_window.height))
                text = pytesseract.image_to_string(screenshot)
                time.sleep(3)
                pyautogui.press('3')
                time.sleep(0.2)
                pyautogui.press('1') #1
        else:
            # Wait before checking again
            time.sleep(1)

if __name__ == "__main__":
    main()
