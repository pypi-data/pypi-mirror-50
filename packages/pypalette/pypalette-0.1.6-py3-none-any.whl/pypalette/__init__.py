# coding:utf-8
__author__ = 'rk.feng'

import base64
import logging
import os
import platform
from ctypes import cdll, c_char_p, c_int
from io import BytesIO

import requests
from PIL import Image

_cur_dir = os.path.dirname(__file__)
_is_linux = platform.system().lower().find("linux") > -1


class ThemeResult(dict):
    """ 主题色结果 """
    Vibrant = "Vibrant"  # 活力
    LightVibrant = "LightVibrant"  # 活力亮
    DarkVibrant = "DarkVibrant"  # 活力暗
    Muted = "Muted"  # 柔和
    LightMuted = "LightMuted"  # 柔和亮
    DarkMuted = "DarkMuted"  # 柔和暗

    @property
    def vibrant(self) -> str:
        return self.get(self.Vibrant)

    @property
    def light_vibrant(self) -> str:
        return self.get(self.LightVibrant)

    @property
    def dark_vibrant(self) -> str:
        return self.get(self.DarkVibrant)

    @property
    def muted(self):
        return self.get(self.Muted)

    @property
    def light_muted(self):
        return self.get(self.LightMuted)

    @property
    def dark_muted(self):
        return self.get(self.DarkMuted)

    def is_valid(self) -> bool:
        keys_set = set(self.keys())
        valid_set = {self.Vibrant, self.LightVibrant, self.DarkVibrant, self.Muted, self.LightMuted, self.DarkMuted}
        return len(keys_set - valid_set) == 0


class ImageThemeTools(object):
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self._dll = None

    def go_calc_palette(self, img_base64: str, max_color_count: int = 8) -> str:
        """ golang  """
        if self._dll is None:
            if _is_linux:
                go_palette = cdll.LoadLibrary(os.path.join(_cur_dir, "go-palette-linux.so"))
            else:
                go_palette = cdll.LoadLibrary(os.path.join(_cur_dir, "go-palette-mac.so"))

            go_palette.CalcPalette.argtypes = [c_char_p, c_int]
            go_palette.CalcPalette.restype = c_char_p
            self._dll = go_palette

        resp = self._dll.CalcPalette(img_base64.encode("utf-8"), max_color_count)
        return resp.decode("utf-8")

    def get_theme_color(self, image: Image.Image, max_color_count: int = None) -> ThemeResult:
        """ 获取主题颜色 """
        # base64
        output_buffer = BytesIO()
        image.save(output_buffer, format='png')
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data).decode("utf-8")

        # 获取结果
        if max_color_count is not None:
            result_str = self.go_calc_palette(img_base64=base64_str, max_color_count=max_color_count)
        else:
            result_str = self.go_calc_palette(img_base64=base64_str)

        # 转为模型
        result_dict = {}
        for line in result_str.split("\n"):
            if len(line) > 2:
                _line_list = line.split("\t")
                assert len(_line_list) == 2
                result_dict[_line_list[0]] = _line_list[1].split("background-color:")[1].split(";")[0]

        return ThemeResult(result_dict)

    def get_theme_color_for_image_path(self, image_path: str, max_color_count: int = None) -> ThemeResult:
        img = Image.open(image_path)
        return self.get_theme_color(image=img, max_color_count=max_color_count)

    def get_theme_color_for_image_url(self, url: str, max_color_count: int = None) -> ThemeResult:
        """ 获取主题颜色 """
        image = Image.open(BytesIO(requests.get(url, timeout=15).content))
        return self.get_theme_color(image=image, max_color_count=max_color_count)

    def theme_visual(self, image_path: str, max_color_count: int = None):
        """ 主题色可视化 """

        # 主题结果
        theme_result = self.get_theme_color_for_image_path(
            image_path=image_path, max_color_count=max_color_count)

        # 打开封面图作为前景色
        img = Image.open(image_path)
        width, height = img.size
        d_width, d_height = int(width * 0.2), int(height * 0.2)

        # 背景图
        bg_img = Image.new('RGB', (width + 2 * d_width, height + 2 * d_height), color=theme_result.muted)

        # 图片合成
        bg_img.paste(img, (d_width, d_height))

        # 图片展示
        bg_img.show()
