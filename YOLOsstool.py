import time
import mss
import cv2
import uuid
import numpy as np
import ctypes
import win32api
import os

print("__  ______  __    ____            __              __")
print(r"\ \/ / __ \/ /   / __ \__________/ /_____  ____  / /")
print(r" \  / / / / /   / / / / ___/ ___/ __/ __ \/ __ \/ / ")
print(" / / /_/ / /___/ /_/ (__  |__  ) /_/ /_/ / /_/ / /  ")
print(r"/_/\____/_____/\____/____/____/\__/\____/\____/_/   ")
print()

# Settings
delay_between_screenshots = 1 # Time between screens (Default 1 sec)
images_folder_path = 'screens' #Foldername

def detect_key_press():
    for vk_code in range(0x08, 0xFF):
        if win32api.GetKeyState(vk_code) & 0x8000:
            return hex(vk_code)
    return None

def get_key_name(key_code):
    key_names = {
        '0x54': 'T', '0x51': 'Q', '0x57': 'W', '0x45': 'E', '0x52': 'R',
        '0x59': 'Y', '0x55': 'U', '0x49': 'I', '0x4F': 'O', '0x50': 'P',
        '0x41': 'A', '0x53': 'S', '0x44': 'D', '0x46': 'F', '0x47': 'G',
        '0x48': 'H', '0x4A': 'J', '0x4B': 'K', '0x4C': 'L',
        '0x5A': 'Z', '0x58': 'X', '0x43': 'C', '0x56': 'V', '0x42': 'B',
        '0x4E': 'N', '0x4D': 'M',
        '0x20': 'SPACEBAR', '0x70': 'F1', '0x71': 'F2', '0x72': 'F3',
        '0x73': 'F4', '0x74': 'F5', '0x75': 'F6', '0x76': 'F7', '0x77': 'F8',
        '0x78': 'F9', '0x79': 'F10', '0x7A': 'F11', '0x7B': 'F12'
    }

    key_code_lower = key_code.lower() if isinstance(key_code, str) else str(key_code).lower()
    return key_names.get(key_code_lower, key_code)

print("> Press any key to set it as your screenshot hotkey.")
print()

keybind = None
while keybind is None:
    detected_key = detect_key_press()
    if detected_key:
        keybind = detected_key
        while detect_key_press() == detected_key:
            time.sleep(0.05)
        break
    time.sleep(0.05)

key_name = get_key_name(keybind)
print(f"> Keybind set to: {key_name}")
print()
print(f"Hold '{key_name}' to take screenshots.")
print(f"A screenshot will be taken every '{delay_between_screenshots}' seconds.")
print()
print("Close the cmd window to stop.")
print()

# pulls screen size
screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)
image_size = screen_height

half_screen_x = int(screen_width / 2)
half_screen_y = int(screen_height / 2)
camera = mss.mss()
pause = number_of_images_taken = 0

box = {
        'left': int(half_screen_x - image_size//2),
        'top': int(half_screen_y - image_size//2),
        'width': int(image_size),
        'height': int(image_size)
    }

if not os.path.exists(images_folder_path):
    print('Creating screenshots folder...')
    os.mkdir('screens')

def hold_down_keybind():
    return win32api.GetKeyState(int(keybind, 16)) in (-127, -128)

while True:
    frame = np.array(camera.grab(box))

    if frame is not None:
        if hold_down_keybind() and time.perf_counter() - pause > 1:
            frame_copy = np.copy(frame)
            cv2.imwrite(f'screens/{str(uuid.uuid4())}.jpg', frame_copy)
            pause = time.perf_counter()
            number_of_images_taken += 1
            print(f'Screenshots taken: {number_of_images_taken}')

    time.sleep(0.001)