import threading
import keyboard
import time
import os
import PySimpleGUI as sg
from pynput.mouse import Listener, Button
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

# define a lock for synchronization
lock = threading.Lock()

def on_mouse_click(x, y, button, pressed):
    global mouse_pressed_left
    if button == Button.left:
        mouse_pressed_left = pressed

def on_press(key):
    global mouse_pressed_left
    if key == Key.mouse_left:
        mouse_pressed_left = True

def on_release(key):
    global mouse_pressed_left
    if key == Key.mouse_left:
        mouse_pressed_left = False

def f5_thread():

    global stop_event
    global mouse_pressed_left

    # define mouse_pressed_left
    mouse_pressed_left = False

    # acquire lock to synchronize access to stop_event
    lock.acquire()
    # reset stop_event to False at the start of the thread
    stop_event = threading.Event()
    # release lock
    lock.release()

    # Read mouse coordinates from file.
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, 'mouse_coordinates.txt')
    with open(file_path, 'r') as file:
        line = file.readline()
        x, y = line.split(',')

    # Convert coordinates to integers.
    x, y = int(x), int(y)

    mouse = MouseController()
    keystroke = KeyboardController()

    mouse_listener = Listener(on_click=on_mouse_click)
    mouse_listener.start()

    keyboard_listener = Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()

    print('Page will begin refreshing in: ')
    for i in range(3, 0, -1):
        print(f"{i}")
        time.sleep(1)

    while not stop_event.is_set():

            # Save current mouse position.
            orig_x, orig_y = mouse.position

            # Simulate left-click at (x,y) coordinates.
            if mouse_pressed_left:
                print('Waiting for the left mouse button to be released...')
                while mouse_pressed_left and not stop_event.is_set():
                    time.sleep(0.1)
            mouse.position = (x, y)
            mouse.press(Button.left)
            mouse.release(Button.left)
            print('Left-clicked at coordinates:', x, y)

            # Simulate F5 key press.
            print('Incoming refresh...')
            keystroke.press(Key.f5)
            keystroke.release(Key.f5)
            print('Page has been Refreshed.')

            # Move mouse back to original position.
            mouse.position = (orig_x, orig_y)
            print('Set mouse to original position:', orig_x, orig_y)

            # Wait for 2 minutes.
            countdown = 120
            while countdown > 0:
                if stop_event.wait(0.1):
                    return
                # Check if any key is pressed. If pressed, add 1 second to the countdown with a maximum of 10 seconds.
                if countdown < 100 and any(keyboard.is_pressed(key) for key in keyboard.all_modifiers.union(set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))):
                    print("User is typing. Adding 1 second to refresh...")
                    countdown = min(countdown + 10, 100)  # Add 1 second to the countdown with a maximum of 10 seconds.
                else:
                    if countdown % 10 == 0:  # Update countdown every 10 iterations (i.e. every 1 second).
                        print('\n' + f'Cooldown: {int(countdown / 10)} seconds')
                    countdown -= 1
                    if mouse_pressed_left and countdown == 0:
                        print('Left mouse button is being held down. Waiting for it to be released...')
                        while mouse_pressed_left and not stop_event.is_set():
                            time.sleep(0.1)
        

        # Reset mouse_pressed_left to False when the thread exits.
        #mouse_pressed_left = False

stop_event = threading.Event()

def on_click(x, y, button, pressed):
    # If the left mouse button is clicked, save the coordinates and stop listening.
    if button == Button.left and pressed:
        # Save coordinates to a file.
        try:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(dir_path, 'mouse_coordinates.txt')
            with open(file_path, 'w') as file:
                file.write(f"{x},{y}")
                print(f"Coordinates ({x}, {y}) saved to {file_path}")
        except Exception as e:
            print(f"Error: {e}")
        return False

def get_coordinates():

    # Give instructions to position mouse and wait for click.
    print('\n' + 'Please position your mouse on the page you wish to monitor and click.' + '\n')
    with Listener(on_click=on_click) as listener:
        listener.join()

def stop_thread():

    stop_event.set()
    print('\n' + 'Script stopped.' + '\n')

    # Remove keyboard hook on exit.
    keyboard.unhook_all()

# Choose a Theme for the Layout
sg.theme('Dark2')

# define GUI layout
layout = [
    [sg.Text("Click 'Get Coordinates' to select the page you wish to automatically refresh.")],
    [sg.Text("You will only need to run this once unless you would like to change which page refreshes.")],
    [sg.Button('Get Coordinates')],
    [sg.Text("")],
    [sg.Text("Click 'Start Refreshing' to begin automatically refreshing the page.")],
    [sg.Button('Start Refreshing'), sg.Button('Stop Refreshing')],
    [sg.Output(size=(70,3))]
]

# create GUI window
window = sg.Window('Refresh-Inator', layout)

# start event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == "Get Coordinates":
        try:
            click_thread = threading.Thread(target=get_coordinates)
            click_thread.start()
        except Exception as e:
            sg.popup(f"Error: {e}")
    if event == "Start Refreshing":
        try:
            five_thread = threading.Thread(target=f5_thread)
            five_thread.start()
        except Exception as e:
            sg.popup(f"Error: {e}")
    if event == "Stop Refreshing":
        try:
            stp_thread = threading.Thread(target=stop_thread)
            stp_thread.start()
        except Exception as e:
            sg.popup(f"Error: {e}")

# close GUI window
window.close()
