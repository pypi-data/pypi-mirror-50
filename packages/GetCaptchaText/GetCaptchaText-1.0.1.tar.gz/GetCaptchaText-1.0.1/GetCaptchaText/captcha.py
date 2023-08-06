# coding:utf-8

import requests
from PIL import Image
import pytesseract


class captcha(object):

    def get_captcha_text(self, image_url, image):
        """
        :return

        返回图片验证码的文本内容(Gets the text content of the image captcha)。

        :param

        image_url: 验证码图片的地址(The address of the captcha picture)

        image: 图片的存放地址(Storage address of pictures)

        :author

        guchen

        """
        r = requests.get(image_url)
        with open(image, 'wb') as f:
            f.write(r.content)
        return pytesseract.image_to_string(Image.open(image).resize((300, 99)))
