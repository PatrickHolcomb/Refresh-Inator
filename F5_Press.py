import threading
import win32api
import win32con
import time
import keyboard

# Read mouse coordinates from file.
with open('mouse_coordinates.txt', 'r') as file:
    line = file.readline()
    x, y = line.split(',')

# Convert coordinates to integers.
x, y = int(x), int(y)

# define f5_thread.
def f5_thread():
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

        time.sleep(0.1)

        # Move mouse back to original position.
        win32api.SetCursorPos((orig_x, orig_y))
        # Simulate left-click at orginal position.
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, orig_x, orig_y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, orig_x, orig_y, 0, 0)
        print('Set mouse to oringinal position:', orig_x, orig_y)


        # Wait for 2 minutes.
        countdown = 1200
        while countdown > 0:
            if stop_event.wait(0.1):
                return
            if keyboard.is_pressed('space'):  # check if space key is pressed.
                print("User is typing. Soft resetting refresh...")
                countdown = 600
            else:
                if countdown % 10 == 0:  # Update countdown every 10 iterations (i.e. every 1 second).
                    print(f'Cooldown: {int(countdown / 10)} seconds')
                countdown -= 1

stop_event = threading.Event()

# Script start delayed slightly.
print('Page will begin refreshing in: ')
for i in range(3, 0, -1):
    print(f"{i}")
    time.sleep(1)

# Start the F5 thread.
f5_thread = threading.Thread(target=f5_thread)
f5_thread.start()

# Listen for the alt key to stop the script.
print("Press alt to stop the script.")
keyboard.wait('alt')
stop_event.set()
print('\n' + 'Script stopped.' + '\n' + 'Have a good one bro.' + '\n')

# Remove keyboard hook on exit.
keyboard.unhook_all()