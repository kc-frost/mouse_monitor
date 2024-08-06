import pystray
from PIL import Image, ImageDraw
from pynput import mouse
import threading

# stop flag
stop_event = threading.Event()

# global variables
mouse_clicks = 0
icon = None
listener = None

def main():
    icon_thread = threading.Thread(target=tray_setup)
    mouse_thread = threading.Thread(target=mouse_listener)
    
    icon_thread.start()
    mouse_thread.start()

    icon_thread.join()
    mouse_thread.join()

# monitoring mouse clicks
def on_click(x, y, button, pressed):
    global mouse_clicks
    if pressed:
        mouse_clicks += 1
        print(mouse_clicks)
        update_icon()

# creating system tray icon
def create_image():
    WIDTH = 64
    HEIGHT = 64
    BLACK = 'black'
    WHITE = 'white'

    # default font size
    font_size = 45

    image = Image.new('RGB', (WIDTH, HEIGHT), BLACK)
    dc = ImageDraw.Draw(image)

    # if number reaches 3 digits, make font smaller
    if len(str(mouse_clicks)) > 2:
        font_size = 35

    dc.text((32,32), str(mouse_clicks), fill=WHITE, anchor="mm", font_size=font_size)

    return image

# updates icon per mouse click
def update_icon():
    if icon:
        icon.icon = create_image()

# quits program when systray's 'exit' is clicked
def on_exit(icon, item):
    stop_event.set()
    icon.stop()

# threads
def tray_setup():
    global icon
    icon = pystray.Icon("Mouse Clicks", create_image(), menu=pystray.Menu(pystray.MenuItem("Exit", on_exit)))
    icon.run()

def mouse_listener(): 
    listener = mouse.Listener(on_click=on_click)
    listener.start()

    # stops when flag turns true
    stop_event.wait()
    listener.stop()

if __name__ == "__main__":
    main()