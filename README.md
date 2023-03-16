# Refresh-Inator

**Description:**

This is a Python script that automates the refreshing of a web page at a specified interval using the win32api library. The script allows the user to select a position on their screen by hovering their mouse over the page they wish to automatically refresh. The position is saved to a file, and the script then uses the saved coordinates to simulate a left-click and F5 key press at that position.

The script also includes a feature to detect if the left mouse button is being held down, and if it is, it delays the refreshing until the button is released. Additionally, if the user types while the countdown is running, the script will add one second to the refresh time, up to a maximum of 10 seconds.

The script includes a simple Graphical User Interface (GUI) that allows the user to easily start and stop the refreshing process. The GUI was created using the PySimpleGUI library.

**Intructions:**
1. Run Refresh-Inator.exe
2. Click 'Get Coordinates' and hover your mouse over the page you wish to auto refresh. (Only needed once unless you would like to change positions.)
3. Click 'Start Refreshing'to begin automatically refreshing the page.
4. Click 'Stop Refreshing' at anytime to cancel auto refresh.
5. Click 'Start Refreshing' if you would like to begin refreshing again.

**Notes:**

• By default, the script is set to refresh the page every two minutes.
• Script will not refresh while User is typing or holding down left click.
