import win32api
import time
import os

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