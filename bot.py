from pynput.keyboard import Key,Listener, Controller
import win32gui
import re
from PIL import ImageGrab
from tkinter import *
from win32gui import FindWindow, GetWindowRect
import tkinter as tk
from PIL import ImageTk
import sys
import time

keyboard = Controller()

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

    def get_rectangle(self):
        win32gui.GetWindowRect(self._handle)

w = WindowMgr()
w.find_window_wildcard(".*Timberman.*")

window_handle = FindWindow(None, "Timberman")
window_rect = GetWindowRect(window_handle)

gameMaxX = window_rect[2]
gameMinX = window_rect[0]
gameMaxY = window_rect[3]
gameMinY= window_rect[1]

gameMiddleX = (window_rect[2] + window_rect[0]) / 2
gameMiddleY = (window_rect[3] + window_rect[1]) / 2

w.set_foreground()
global px
px = ImageGrab.grab(window_rect)

root = tk.Tk()
label = tk.Label(root)
label.pack()
img = None
tkimg = [None] 
global stop
global start
global lastPressedKey
start = False
stop = False

def on_press(key):
    global lastPressedKey
    global img
    global px
    global start
    
    global stop
    if key == Key.esc:
        stop = True
        return

    key = str(key).replace("'",'')
    lastPressedKey = key
    keyboard.release(key)
    if str(key) == 'a' or key == 'd':
        start = True
        px = ImageGrab.grab(window_rect)
        img = ImageTk.PhotoImage(px)
        #px.save('bot.png')


listener = Listener(on_press=on_press)
listener.start()

delay = 100
def loopCapture():
    global img
    global px
    global start
    if stop == False:
        pixels = px.load()
        rightPixel = str(pixels[585,379])
        leftPixel = str(pixels[444,392])

        if rightPixel != '(2, 1, 0)' and rightPixel != '(7, 1, 2)' and rightPixel != '(4, 5, 5)':
            #print('escapeFromRight!')
            keyboard.press('a')
        elif leftPixel != '(2, 1, 0)' and leftPixel != '(7, 1, 2)' and leftPixel != '(4, 5, 5)':
           #print('escapeFromLeft!')
            keyboard.press('d')
        else:
            keyboard.press(lastPressedKey)
            
        label.config(image=img)
        root.update_idletasks()
        root.after(delay, loopCapture)

    else:
        sys.exit()

while True:
    if start == True:
        break
    pass

loopCapture()
root.mainloop()
