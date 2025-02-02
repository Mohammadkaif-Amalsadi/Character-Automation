import cv2
import numpy as np
from PIL import ImageGrab
import tkinter as tk
import win32gui
import pytesseract
import time
import keyboard
import pygame
import difflib
import traceback

pygame.mixer.init()
# Path to Tesseract executable (update this with your own path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# List of all Pokémon names (expand this list as needed)
all_pokemon_names = ["Bulbasaur", "Charmander","Magikarp","Scyther","Pinsir","Heracross","Nincada","Joltik","Larvesta","Dwebble","Cutiefly", 
                     "Squirtle", "Shroomish", "Absol","Dratini",
                     "Pikachu", "Raichu", "Abra", "Gible", "Mimikyu", "Buneary", "Mawile", "Hawlucha", 
                     "Skarmory", "Larvesta","Litwick", "Sableye", "Riolu", "Electrike", "Ralts", "Drilbur", "Blacephalon", "Sneasel","Spheal","Marill", "Gliger"]

# Function to correct the detected Pokémon name
def correct_pokemon_name(detected_name):
    closest_matches = difflib.get_close_matches(detected_name, all_pokemon_names, n=1, cutoff=0.6)
    if closest_matches:
        return closest_matches[0]  # Return the closest match
    return detected_name  # If no close match, return the detected name as is

# Function to check if a certain text is present in the OCR result
def is_text_present(ocr_result, target_text):
    return target_text.lower() in ocr_result.lower()

# Function to get the dimensions of the window with the specified title
def get_window_rect(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    rect = win32gui.GetWindowRect(hwnd)
    return rect

# Function to perform OCR on the given image
def perform_ocr(image):
    ocr_result = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
    return ocr_result

# Function to check if the detected Pokémon name is in the list of target Pokémon names
def check_target_pokemon(target_names, detected_name):
    for name in target_names:
        if name.lower() in detected_name.lower():
            return True
    return False

# Function to stop the sound
def stop_sound():
    sound.stop()
    label.config(text="Sound Stopped")
    root.update()

# Function to monitor the screen for the target text
def monitor_screen(window_title, target_pokemon):
    global sound, label, root

    # Load the sound file
    sound = pygame.mixer.Sound("mixkit-alarm-tone-996.wav")
    sound_playing = False

    while True:
        try:
            rect = get_window_rect(window_title)
            if rect != (0, 0, 0, 0):
                screenshot = np.array(ImageGrab.grab(bbox=rect))
                screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

                # Perform OCR on the screenshot
                ocr_result = perform_ocr(screenshot_gray)

                # Check if the target text is present
                if is_text_present(ocr_result, "You encountered"):
                    pokemon_name = ocr_result.split("You encountered ")[1].split()[0]
                    
                    # Correct the detected Pokémon name
                    corrected_name = correct_pokemon_name(pokemon_name)

                    label.config(text="You encountered " + corrected_name + " (Target found)")
                    root.update()

                    if "shiny" in ocr_result.lower():
                        label.config(text="You encountered a shiny " + corrected_name + " (Target found)")
                        root.update()

                    if not sound_playing:
                        # Play the sound
                        sound.play(-1)  # -1 loops the sound indefinitely
                        sound_playing = True
                    # Stop pressing Ctrl
                    keyboard.release('ctrl')
                    # Wait for 5 seconds to avoid detecting the same encounter repeatedly
                    time.sleep(5)

                elif is_text_present(ocr_result, "Wild"):
                    wild_pokemon_name = ""
                    wild_split = ocr_result.split("Wild ")
                    if len(wild_split) > 1:
                        wild_pokemon_name = wild_split[1].split()[0]

                        # Correct the detected Pokémon name
                        corrected_wild_name = correct_pokemon_name(wild_pokemon_name)

                        # Check if the detected Pokémon is in the list of target Pokémon
                        if check_target_pokemon(target_pokemon, corrected_wild_name):
                            label.config(text="Found " + corrected_wild_name + " (Target found)")
                            root.update()

                            if not sound_playing:
                                # Play the sound
                                sound.play(-1)  # -1 loops the sound indefinitely
                                sound_playing = True
                        else:
                            label.config(text="Found " + corrected_wild_name + " (not the target)")
                            root.update()
                            sound.stop()  # Stop the sound
                            sound_playing = False
                            # Press Ctrl until the label disappears
                            while label['text'] == "Found " + corrected_wild_name + " (not the target)":
                                keyboard.press('ctrl')
                                keyboard.release('ctrl')
                                time.sleep(1)
                                keyboard.press('ctrl')
                                keyboard.release('ctrl')
                                time.sleep(1)
                                keyboard.press('ctrl')
                                keyboard.release('ctrl')
                                time.sleep(1)
                                # Update the label text in case the target Pokémon is found during the loop
                                if is_text_present(perform_ocr(screenshot_gray), "Wild"):
                                    break
                else:
                    label.config(text="")
                    root.update()
                    sound.stop()  # Stop the sound
                    sound_playing = False
            else:
                label.config(text="PROClient window not found")
                root.update()
                sound.stop()  # Stop the sound
                sound_playing = False
        except Exception:
            print("An error occurred:")
              # Print the exception message
             # Print the stack trace
            # Stop the sound and update the label
            sound.stop()
            label.config(text="An error occurred. Restarting...")
            root.update()
            time.sleep(5)  # Wait for 5 seconds before restarting
            continue

        # Add a delay to reduce CPU load
        time.sleep(1)

# Create a tkinter window for displaying the label
root = tk.Tk()
root.title("PROClient Monitor")
root.attributes('-alpha', 1.0)  # Set transparency to 0% (fully visible)
root.attributes('-topmost', True)  # Set the window to be always on top

# List of target Pokémon names
target_pokemon = ["Charmander","Larvesta","Litwick","Magikarp","Absol","Dratini","Blacephalon", "Sneasel", "Mimikyu", "Buneary", "Shroomish", "Mawile", "Hawlucha", "Skarmory", "Sableye", "Riolu", "Abra", "Gible", "Electrike", "Ralts", "Drilbur", "Gliger"]
# target_pokemon = ["Scyther","Pinsir","Heracross","Nincada","Joltik","Larvesta","Dwebble","Cutiefly","Basculin","Wishiwashi","Relicanth","Feebas","Carvanha"]

# Create a label for displaying the message
label = tk.Label(root, text="", font=("Helvetica", 16))
label.pack()

# Add a stop button
stop_button = tk.Button(root, text="Stop Sound", command=stop_sound)
stop_button.pack()

# Start monitoring the screen for the target text
monitor_screen("PROClient", target_pokemon)

root.mainloop()
