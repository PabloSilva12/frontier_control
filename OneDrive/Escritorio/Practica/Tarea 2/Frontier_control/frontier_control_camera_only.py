import cv2
from datetime import datetime
import os
import pygame
import sys
import threading
from pynput import keyboard
import cv2
from datetime import datetime
import serial
import time

pygame.init()

arduino_port = "COM3"
try:
    ser = serial.Serial(arduino_port, 9600, timeout=1)
except:
    print("no hay arduino conectado")

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Mapping for special characters
special_characters_mapping = {
    pygame.K_HASH: "#",
    pygame.K_UNDERSCORE: "_",
}

def send_command(command):
    ser.write(command.encode())  
    time.sleep(1)

def convert_special_characters(data):
    for key, value in special_characters_mapping.items():
        data = data.replace(chr(key), value)
    return data

def get_scanner_code(scanned_data_container):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    scanned_data = ""
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
def on_press(key):
    try:
        scanned_data_container.append(key.char)
    except AttributeError:
        scanned_data_container.append(str(key))

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def save_image(scanner_code, frame):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f'{scanner_code}_{formatted_datetime}.png'

    # Ensure the "images" directory exists
    if not os.path.exists('images'):
        os.makedirs('images')

    cv2.imwrite(os.path.join('images', filename), frame)
    print(f"Image saved as {filename}")

scanned_data_container = []
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

while True:
    if scanned_data_container:
        try:
            send_command(1)
        except:
            print("no se puede abrir barrera")
        scanner_code = ''.join(scanned_data_container)
        ret, frame = cv2.VideoCapture(0, cv2.CAP_DSHOW).read()
        save_image(scanner_code, frame)
        scanned_data_container.clear()
