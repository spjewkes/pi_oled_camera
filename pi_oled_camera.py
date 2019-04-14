#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

try:
    from picamera import PiCamera
except ImportError:
    exit('This script requires the picamera module\nInstall with: sudo pip install picamera')

class OledBoard:
    '''
    Define a class that manages the AdaFruit OLED board
    '''
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

        self.A = OledBoard.setup_input(board.D5)
        self.B = OledBoard.setup_input(board.D6)
        self.C = OledBoard.setup_input(board.D4)
        self.UP = OledBoard.setup_input(board.D17)
        self.DOWN = OledBoard.setup_input(board.D22)
        self.LEFT = OledBoard.setup_input(board.D27)
        self.RIGHT = OledBoard.setup_input(board.D23)

        self.clear()

        # Setup image and draw object to display to screen
        self.width = self.disp.width
        self.height = self.disp.height
        
    @staticmethod
    def setup_input(pin):
        instance = DigitalInOut(pin)
        instance.direction = Direction.INPUT
        instance.pull = Pull.UP
        setattr(instance, 'pressed', False)
        setattr(instance, 'released', False)
        return instance
        
    def __del__(self):
        self.disp.poweroff()        
        
    def clear(self):
        self.disp.fill(0)
        self.disp.show()

    @staticmethod
    def check_key(key):
        if not key.value:
            key.pressed = True
            key.released = False
        elif key.value and key.pressed:
            key.pressed = False
            key.released = True
        else:
            key.pressed = False
            key.released = False

    def write(self, buf):
        img = Image.frombytes('RGB', (256, 256), buf)
        img = img.resize((128, 64), Image.BILINEAR)
        img = img.convert('1')

        self.disp.image(img)
        self.disp.show()

    def loop(self):

        while not self.A.released:
            OledBoard.check_key(self.A)
            OledBoard.check_key(self.B)
            OledBoard.check_key(self.C)
            OledBoard.check_key(self.UP)
            OledBoard.check_key(self.DOWN)
            OledBoard.check_key(self.LEFT)
            OledBoard.check_key(self.RIGHT)

def main():
    
    with PiCamera() as camera:
        
        camera.resolution = (256, 256)
        camera.contrast = 50
        camera.rotation = 90
        camera.start_preview()

        camOut = OledBoard()
        camera.start_recording(camOut, 'rgb')

        try:
            camOut.loop()

        finally:
            camera.stop_recording()

if __name__ == "__main__":
    main()        
