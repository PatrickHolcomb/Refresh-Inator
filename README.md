# Refresh-Inator

*Description:*
These scripts serve to automate the process of refreshing a web page by simulating a left-click and F5 key press.

The first script called Get_Mouse_Coordinates.py saves the current position of the mouse cursor in a file named mouse_coordinates.txt, which will be used by the second script called F5_Press.py to simulate a left-click at those coordinates. This script waits for the user to position their mouse cursor on the page they want to monitor, counts down from 5, gets the current mouse coordinates using the win32api.GetCursorPos() function, and then saves the coordinates to the file.

The second script reads the saved coordinates from the mouse_coordinates.txt file, and then creates a new thread to run the f5_thread() function. This function simulates a left-click at the saved coordinates, then simulates an F5 key press to refresh the page. After simulating an F5 key press it sets the mouse cursor back to its original position and simulates a left-click at that position so that the window the user is using remains active. It then waits for 2 minutes, while checking for any spacebar presses from the user to reset the cooldown period. This is to remove the possibility of the script inturpting the user while they are typing. This process repeats until the stop_event is set. The stop_event is triggered by an 'alt' key press which can be done at any time by the user. The keyboard.unhook_all() function is called to remove the keyboard hook on exit.

*Intructions:*
1. Run the Get_Mouse_Coordinates.py file. (Only needed once unless the coordinates need to be updated.)
2. Position your mouse on the page you wish to monitor within the 5 second time limit.
3. Run the F5_Press.py file using the Python Debug Console. (So far during testing the script fails to work using the normal Python Terminal.)
4. Press the ‘alt’ key at any time to abort the script.

*Notes:*
• Running the Get_Mouse_Coordinates.py file will only be needed once unless you would like to change the webpage you refresh or have changed the webpages position.
• By default, the script is set to refresh the page every two minutes.
• Each time the space bar is pressed the cooldown is soft reset to 1 minute.
• The script detects the space bar no matter the condition while it is running.
• You do not need to be within the console to abort the script with the ‘alt’ key.
