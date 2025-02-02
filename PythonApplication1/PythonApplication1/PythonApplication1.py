import tkinter as tk
from tkinter import filedialog
import random
import time
import threading
import keyboard
import win32gui

class PokemonHunterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon Hunter")
        
        self.create_widgets()
        self.is_hunting = False
        self.target_window_title = "PROClient"  # Define your target window title

    def create_widgets(self):
        # Upload Button
        self.upload_button = tk.Button(self.root, text="Upload Target Pokemon", command=self.upload_pokemon)
        self.upload_button.pack(pady=10)

        # Start Button
        self.start_button = tk.Button(self.root, text="Start Hunting", command=self.start_hunting)
        self.start_button.pack(pady=5)

        # Stop Button
        self.stop_button = tk.Button(self.root, text="Stop Hunting", command=self.stop_hunting, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

    def upload_pokemon(self):
        file_path = filedialog.askopenfilename(title="Select Target Pokemon Image")
        if file_path:
            print("Uploaded Pokemon:", file_path)  # You can handle the uploaded file here
    
    def start_hunting(self):
        print("Hunting Started")
        # Implement your hunting logic here
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.is_hunting = True

        self.hunting_thread = threading.Thread(target=self.simulate_key_press)
        self.hunting_thread.start()

    def stop_hunting(self):
        print("Hunting Stopped")
        # Implement your stop logic here
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.is_hunting = False

    def is_target_window_active(self):
        active_window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        return active_window_title == self.target_window_title

    def simulate_key_press(self):
        while self.is_hunting:
            if self.is_target_window_active():
                for _ in range(random.randint(5, 10)):  # Randomly press 'A' multiple times
                    if not self.is_hunting:
                        break
                    keyboard.press('a')
                    time.sleep(0.01)  # Adjust the delay between key presses if needed
                    keyboard.release('a')

                for _ in range(random.randint(5, 10)):  # Randomly press 'D' multiple times
                    if not self.is_hunting:
                        break
                    keyboard.press('d')
                    time.sleep(0.01)  # Adjust the delay between key presses if neededd
                    keyboard.release('d')   
            else:
                time.sleep(1)  # If the target window is not active, wait for a second before checking again

if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonHunterApp(root)
    root.mainloop()
