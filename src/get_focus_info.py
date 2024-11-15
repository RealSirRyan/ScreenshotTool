from Xlib import display
from time import sleep
from main import get_focus_window

d = display.Display()

def get_focus_info():
    focus = get_focus_window()
    
    if focus:
        class_info = focus.get_wm_class()

        return class_info


#Constantly print infomation about the focus window
if __name__ == "__main__":
    while True:
        
        class_info = get_focus_info()

        if class_info:
            print('App Name 1: '+ class_info[0])
            print('App Name 2: '+ class_info[1])
           
        sleep(1)

        