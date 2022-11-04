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
        Clock.schedule_interval(self.start, 0.5)

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
        npimg = np.array(image)
        # ocvim = cv.cvtColor(npimg, cv.COLOR_RGB2BGR)
        ocvim = cv.cvtColor(npimg, cv.COLOR_BGR2GRAY)

        # pegando apenas a linha central da imagem
        height, width = ocvim.shape[:2]
        start_row, start_col = 0, int(width * 0.5 - 50)
        end_row, end_col = height, int(width * 0.5 + 50)
        # faixa = ocvim[start_row:end_row, start_col:end_col]
        # cv.imwrite("faixa.png", faixa)

        DIVISOES = height / 3
        end_h_1 = int(DIVISOES)
        ped_1 = ocvim[start_row:end_h_1, start_col:end_col]
        # cv.imwrite("pedaco_1.png", ped_1)

        end_h_2 = int(2 * DIVISOES)
        ped_2 = ocvim[end_h_1:end_h_2, start_col:end_col]
        # cv.imwrite("pedaco_2.png", ped_2)

        end_h_3 = int(3 * DIVISOES)
        ped_3 = ocvim[end_h_2:end_h_3, start_col:end_col]
        # cv.imwrite("pedaco_3.png", ped_3)

        # DIVISOES = 3
        # end_h_1 = int(height / DIVISOES)
        # pedaco_1 = ocvim[start_row:end_row, end_h_1:2*end_h_1]
        # # pedaco_1 = ocvim[end_h_1 : 2 * end_h_1, start_row:end_row]
        # cv.imwrite("pedaco_1.png", pedaco_1)

        # start_row, start_col = int(height * 0.5 - 50), 0
        # end_row, end_col = int(height * 0.5 + 50), width

        # dividir imagem em 3
        # DIVISOES = 3
        # end_w_1 = int(width / DIVISOES)
        # pedaco_1 = ocvim[start_row:end_row, 0:end_w_1]
        # start_row, start_col = int(height * 0.5 - 50), 0
        # end_row, end_col = int(height * 0.5 + 50), width
        # cropped = ocvim[start_row:end_row, start_col:end_col]
        # cv.imwrite("inteira.png", ocvim)

        # dividir a imagem em 5 pedaços
        # end_wdh_1 = int(width / 3)
        # pedaco_1 = ocvim[start_row:end_row, 0:end_wdh_1]
        # # cv.imwrite("pedaco_1.png", pedaco_1)

        # start_wdh_2 = end_wdh_1 + 1
        # end_wdh_2 = int(width * 2 / 3)
        # pedaco_2 = ocvim[start_row:end_row, start_wdh_2:end_wdh_2]
        # # cv.imwrite("pedaco_2.png", pedaco_2)

        # start_wdh_3 = end_wdh_2 + 1
        # pedaco_3 = ocvim[start_row:end_row, start_wdh_3:width]
        # cv.imwrite("pedaco_3.png", pedaco_3)

        # verificando a media dos pixels da imagem
        # white = 1, black = 0

        LUMUS = 64
        result_1 = 1 if int(np.mean(ped_1)) >= LUMUS else 0
        result_2 = 1 if int(np.mean(ped_2)) >= LUMUS else 0
        result_3 = 1 if int(np.mean(ped_3)) >= LUMUS else 0

        # # return f"r1:{result_1}, r2: {result_2}, r3: {result_3}"
        return f"{result_3}{result_2}{result_1}"

    def serialCommunication(self, data: str):
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

        # serial_port.close()  # essa funcao esta quebrando o app


class TestCamera(App):
    def build(self):
        return CameraClick()


TestCamera().run()
