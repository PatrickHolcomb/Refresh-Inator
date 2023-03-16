import threading
import win32api
import win32con
import keyboard
import time
import os
import PySimpleGUI as sg

# define a lock for synchronization
lock = threading.Lock()

# define f5_thread.
def f5_thread():

    global stop_event
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

    print('Page will begin refreshing in: ')
    for i in range(3, 0, -1):
        print(f"{i}")
        time.sleep(1)

    while not stop_event.is_set():

        # Save current mouse position.
        orig_x, orig_y = win32api.GetCursorPos()

        # Simulate left-click at (x,y) coordinates.
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        print('Left-clicked at coordinates:', x, y)

        # Simulate F5 key press.
        print('Incoming refresh...')
        win32api.keybd_event(win32con.VK_F5, 0, 0, 0)
        win32api.keybd_event(win32con.VK_F5, 0, win32con.KEYEVENTF_KEYUP, 0)
        print('Page has been Refreshed.')

        # Move mouse back to original position.
        win32api.SetCursorPos((orig_x, orig_y))
        print('Set mouse to oringinal position:', orig_x, orig_y)


        # Wait for 2 minutes.
        countdown = 1200
        left_click_held = False  # track whether left click is held down.
        while countdown > 0:
            if stop_event.wait(0.1):
                return
            # Check if any key is pressed. If pressed, add 1 second to the countdown with a maximum of 10 seconds.
            if countdown < 100 and any(keyboard.is_pressed(key) for key in keyboard.all_modifiers.union(set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))):
                print("User is typing. Adding 1 second to refresh...")
                countdown = min(countdown + 10, 100)  # Add 1 second to the countdown with a maximum of 10 seconds.
                left_click_held = False  # reset left_click_held.
            else:
                if countdown % 10 == 0:  # Update countdown every 10 iterations (i.e. every 1 second).
                    print(f'Cooldown: {int(countdown / 10)} seconds')
                countdown -= 1

            if countdown == 0:
                # Check if left mouse button is down.
                if win32api.GetKeyState(win32con.VK_LBUTTON) < 0:
                    if not left_click_held:
                        left_click_held = True  # mark left click as held down
                        print('Left mouse button is down, delaying countdown...')
                        while win32api.GetKeyState(win32con.VK_LBUTTON) < 0:
                            time.sleep(0.1)
                            if stop_event.wait(0.1):
                                return
                            # continue checking if left mouse button is being held down.
                    else:
                        # left mouse button is already marked as held down, continue checking.
                        time.sleep(3)
                else:
                    if left_click_held:
                        print('Left mouse button is released, resuming countdown...')
                        left_click_held = False  # mark left click as released
                    else:
                        break

stop_event = threading.Event()

def coordinate_thread():

    # Get full path to mouse_coordinates.txt.
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, 'mouse_coordinates.txt')

    # Give time to position mouse.
    print('Please position your mouse on the page you wish to monitor.')
    for i in range(5, 0, -1):
        print(f"{i} seconds left")
        time.sleep(1)

    # Get current mouse coordinates.
    x, y = win32api.GetCursorPos()

    # Save coordinates to a file.
    try:
        with open(file_path, 'w') as file:
            file.write(f"{x},{y}")
            print(f"Coordinates ({x}, {y}) saved to {file_path}")
    except Exception as e:
        print(f"Error: {e}")

def stop_thread():

    stop_event.set()
    print('\n' + 'Script stopped.' + '\n')

    # Remove keyboard hook on exit.
    keyboard.unhook_all()

# Choose a Theme for the Layout
sg.theme('Dark2')

# define GUI layout
layout = [
    [sg.Text("Click 'Get Coordinates' and hover your mouse over the page you wish to automatically refresh.")],
    [sg.Text("You will only need to run this once unless you would like to change which page refreshes.")],
    [sg.Button('Get Coordinates')],
    [sg.Text("")],
    [sg.Text("Click 'Start Refreshing' to begin automatically refreshing the page.")],
    [sg.Button('Start Refreshing'), sg.Button('Stop Refreshing')],
    [sg.Output(size=(80,20))]
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
            coord_thread = threading.Thread(target=coordinate_thread)
            coord_thread.start()
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
