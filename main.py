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

# from select import selectNov 3 9:00 PM
from traceback import print_tb
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.camera import Camera
import cv2 as cv
import numpy as np
from PIL import Image

Builder.load_string(
    """
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (1280, 720)
        play: False
        canvas.before:
            PushMatrix
            Rotate:
                angle: -90
                origin: self.center
        canvas.after:
            PopMatrix
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.pre_start()
"""
)


class CameraClick(BoxLayout):
    def pre_start(self):
        Clock.schedule_interval(self.start, 0.005)

    def start(self, dt):
        image = self.capture()
        result = self.handleImgOpenCV(image)
        self.serialCommunication(result)
        print(result)

    def capture(self) -> Image:
        # referencia da camera
        camera: Camera = self.ids["camera"]

        pil_image: Image = Image.frombytes(
            mode="RGBA", size=camera.texture.size, data=camera.texture.pixels
        )

        return pil_image

    def handleImgOpenCV(self, image: Image) -> str:
        # convertendo buffer de bytes para imagem pil

        # convertando para um formato usado pelo opencv
        img = np.array(image)
        # ocvim = cv.cvtColor(npimg, cv.COLOR_RGB2BGR)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, img_bw = cv.threshold(img_gray, 32, 255, cv.THRESH_BINARY)

        height, width = img_bw.shape[:2]

        start_row, start_col = 0, int(width * 0.5 - 50)
        end_row, end_col = height, int(width * 0.5 + 50)

        img_to_slice = img_bw

        NUM_SLICES = 5
        SLICES_SIZE = int(height / NUM_SLICES)

        result_has_black = ""

        for i in range(NUM_SLICES):
            start_row = SLICES_SIZE * i
            end_row = SLICES_SIZE * (i + 1)

            slice = img_to_slice[start_row:end_row, start_col:end_col]

            # extract and count all pixels from slice image whose pixel value is 0
            num_black_pixels = np.sum(slice == 0)

            # print(f'slice{i+1}: {slice}')

            has_black = "1" if num_black_pixels > 0 else "0"

            result_has_black += has_black

        return f"<{result_has_black}>"

    def serialCommunication(self, data: str):
        from usb4a import usb
        from usbserial4a import serial4a

        # preparando para enviar dados pela serial
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
                serial_port.write(bytes(data, "utf-8"))


class TestCamera(App):
    def build(self):
        return CameraClick()


TestCamera().run()
