"""
Camera Example
==============

This example demonstrates a simple use of the camera. It shows a window with
a buttoned labelled 'play' to turn the camera on and off. Note that
not finding a camera, perhaps because gstreamer is not installed, will
throw an exception during the kv language processing.

"""

# Uncomment these lines to see all the messages
# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.image import Image

import cv2 as cv

from usb4a import usb
from usbserial4a import serial4a

Builder.load_string(
    """
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (1280, 720)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
"""
)


class CameraClick(BoxLayout):
    def capture(self):
        usb_device_list = usb.get_usb_device_list()

        if usb_device_list:
            serial_port = serial4a.get_serial_port(
                usb_device_list[0].getDeviceName(),
                9600,  # Baudrate
                8,  # Number of data bits(5, 6, 7 or 8)
                "N",  # Parity('N', 'E', 'O', 'M' or 'S')
                1,
            )  # Number of stop bits(1, 1.5 or 2)
            if serial_port and serial_port.is_open:
                serial_port.write(b"Hello world!")
                # serial_port.close()


class TestCamera(App):
    def build(self):
        return CameraClick()


TestCamera().run()
