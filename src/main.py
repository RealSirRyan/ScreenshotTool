from Xlib import display
from PIL import Image
import pyautogui
import os
import datetime
import fnmatch
import subprocess
import io


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
        width += x
        x = 0
    if y < 0:
        height += y
        y = 0

    return x, y, width, height




def main():

    overrides = {
        'minecraft*': 'Minecraft', #Minecraft adds the version number to end. This way, there won't be a different directory for each version
        'nemo-desktop': '',
    }

    screenshots_dir = os.path.expanduser('~/Desktop/screenshots')
    
    #Todo: This assumes focus_window exists
    focus_window = get_focus_window()
    
    app_name = focus_window.get_wm_class()[1]
    x, y, width, height = get_geometry(focus_window)
    
    print('App: ', app_name)
    print(f'Geometry: ({x}, {y}, {width}, {height})')

    #Check if there is an override for app_name
    for old, new in overrides.items():
        if fnmatch.fnmatch(app_name.lower(), old.lower()):
            app_name = new
            print('App name override: ', app_name)
            break

    #Take a screenshot
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(f'{screenshots_dir}/{app_name}', exist_ok=True)
    screenshot.save(f'{screenshots_dir}/{app_name}/{file_name}.png')

    #Copy to clipboard
    '''image_bytes = io.BytesIO()
    screenshot.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i'], input=image_bytes.read())'''

if __name__ == "__main__":
    main()