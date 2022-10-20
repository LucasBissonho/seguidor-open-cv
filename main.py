'''
Camera Example
==============

This example demonstrates a simple use of the camera. It shows a window with
a buttoned labelled 'play' to turn the camera on and off. Note that
not finding a camera, perhaps because gstreamer is not installed, will
throw an exception during the kv language processing.

'''

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
import time

Builder.load_string('''
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
''')


class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera: Camera = self.ids['camera']
        # timestr = time.strftime("%Y%m%d_%H%M%S")
        # camera.export_to_png("IMG_{}.png".format(timestr))
        camera.export_to_png("IMG.png")

        img_read = cv.imread("IMG.png", cv.IMREAD_GRAYSCALE)

        if img_read.any():
            cv.imshow("image", img_read)

            cv.waitKey(0)
 
            # It is for removing/deleting created GUI window from screen
            # and memory
            cv.destroyAllWindows()
        else:
            print('deu ruim')


class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()