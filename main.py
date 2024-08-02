import pystray
from PIL import Image, ImageDraw
from pynput import mouse
import threading

# global variables
mouse_clicks = 0
icon = None

def main():
    mouse_thread()
    tray_thread()

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

    image = Image.new('RGB', (WIDTH, HEIGHT), BLACK)
    dc = ImageDraw.Draw(image)

    dc.text((32,32), str(mouse_clicks), fill=WHITE, anchor="mm", font_size=45)

    return image

# updates icon per mouse click
def update_icon():
    if icon:
        icon.icon = create_image()

# threads
def tray_thread():
    global icon
    icon = pystray.Icon("Mouse Clicks",create_image())
    tray_thread = threading.Thread(target=icon.run)
    tray_thread.start()

def mouse_thread(): 
    listener = mouse.Listener(
    on_click=on_click)
    listener.start()

main()