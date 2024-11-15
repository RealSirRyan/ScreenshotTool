import Xlib
from Xlib import display
from PIL import Image
import pyautogui
from time import sleep


#Get the focus window
def get_focus_window():
    d = display.Display()
    window = d.get_input_focus().focus

    while window:
        if window.get_wm_class():
            return window

        elif window == d.screen().root:
            return None
        else:
            window = window.query_tree().parent

def get_geometry(focus_window):
    child_geometry = focus_window.get_geometry()
    parent_geometry = focus_window.query_tree().parent.get_geometry()

    x, y, width, height = parent_geometry.x+child_geometry.x, parent_geometry.y+child_geometry.y, child_geometry.width, child_geometry.height

    #Don't want to capture out of bounds areas
    if x < 0:
        width -= abs(x)
        x = 0
    if y < 0:
        height -= abs(y)
        y = 0

    return x, y, width, height


#TODO: Get parent window geometry




def main():
    #1 - Identify the active window.
    #Todo: This assumes focus_window exists
    
    
    focus_window = get_focus_window()
    
    app_name = focus_window.get_wm_class()[1]
    
    

    x, y, width, height = get_geometry(focus_window)
    
    print('App: ', app_name)
    print(f'Geometry: ({x}, {y}, {width}, {height})')

    #4 - Take a screenshot
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    screenshot.show()


if __name__ == "__main__":
    main()