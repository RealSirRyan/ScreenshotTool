from Xlib import display
import pyautogui
import os
import datetime
import fnmatch
import subprocess
import io
import sys


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
    
    screen_width = pyautogui.size().width
    screen_height = pyautogui.size().height
    
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
    
    if x + width > screen_width:
        width = screen_width - x
    if y + height > screen_height:
        height = screen_height - y

    return x, y, width, height

def main():

    '''
    Screenshot types:
        window
        desktop
        snip
    '''
    #Getting arguments
    args = sys.argv
    print(args)
    if len(args) < 2:
        screenshot_type = 'window'
    else:
        screenshot_type = args[1]

    overrides = {
        'minecraft*': 'Minecraft', #Minecraft adds the version number to end. This way, there won't be a different directory for each version
        'nemo-desktop': '',
    }

    screenshots_dir = os.path.expanduser('~/Pictures/Screenshots')
    
    
    #Do something different depending on what screenshot type it is
    if screenshot_type == 'window' or screenshot_type == 'snip':
        #Todo: This assumes focus_window exists
        focus_window = get_focus_window()
        
        app_name = focus_window.get_wm_class()[1].capitalize()
        x, y, width, height = get_geometry(focus_window)
        
        print('App: ', app_name)
        print(f'Geometry: ({x}, {y}, {width}, {height})')

        #Check if there is an override for app_name
        for old, new in overrides.items():
            if fnmatch.fnmatch(app_name.lower(), old.lower()):
                app_name = new
                print('App name override: ', app_name)
                break
    
    elif screenshot_type == 'desktop':
        x, y, width, height = 0, 0, pyautogui.size().width, pyautogui.size().height
        app_name = ''
   
    else:
        raise ValueError('Invalid screenshot type')
    
    os.makedirs(f'{screenshots_dir}/{app_name}', exist_ok=True)

    
    if screenshot_type == 'snip':
        #Use fireshot to take a snippet
        subprocess.run(['flameshot', 'gui', '--clipboard', '--path', f'{screenshots_dir}/{app_name}'])
        pass
    else:
        #Take a screenshot
        screenshot = pyautogui.screenshot(region=(x, y, width, height))

        file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot.save(f'{screenshots_dir}/{app_name}/{file_name}.png')

        #Copy to clipboard
        image_bytes = io.BytesIO()
        screenshot.save(image_bytes, format='PNG')#Save to BytesIO object (in memory)
        image_bytes.seek(0)#Move to beginning of BytesIO object
        subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i'], input=image_bytes.read())#Copy to clipboard

if __name__ == "__main__":
    main()