# Refresh-Inator

**Description:**

This script allows you to automatically refresh a web page by simulating a left-click and F5 keypress every two minutes. You can select which page to monitor by clicking on it with the left mouse button. The script also allows you to stop the automatic refreshing.

The script uses the pynput library to listen for left mouse clicks and keyboard events. When the left mouse button is clicked, the script saves the coordinates to a file. When the script is running, it reads the coordinates from the file and simulates a left-click and F5 keypress at those coordinates every two minutes.

The GUI is created using the PySimpleGUI library. The GUI has two buttons: "Get Coordinates" and "Start Refreshing". The "Get Coordinates" button opens a new window with instructions to position the mouse on the page to be monitored and click. The "Start Refreshing" button starts the automatic refreshing.

The script also allows the user to stop the automatic refreshing by clicking a "Stop" button. When the "Stop" button is clicked, the script sets a stop_event, which stops the while loop in the f5_thread function. The script also unregisters the keyboard hook.

**Intructions:**
1. Run Refresh-Inator.exe
2. Click 'Get Coordinates' and click the page you wish to auto refresh. (Only needed once unless you would like to change positions.)
3. Click 'Start Refreshing'to begin automatically refreshing the page.
4. Click 'Stop Refreshing' at anytime to cancel auto refresh.
5. Click 'Start Refreshing' if you would like to begin refreshing again.

**Notes:**

• By default, the script is set to refresh the page every two minutes.

• Script will not refresh while User is typing or holding down left click.
