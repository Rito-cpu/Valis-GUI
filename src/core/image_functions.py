import os

from .app_config import *


class Functions:
    # SET SVG ICON
    def set_svg_icon(icon_name):
        svg_icon_folder = os.path.abspath(os.path.join(IMG_RSC_PATH, "svg_icons"))
        icon = os.path.abspath(os.path.join(svg_icon_folder, icon_name))
        return icon

    # SET SVG IMAGE
    def set_svg_image(image_name):
        svg_image_folder = os.path.abspath(os.path.join(IMG_RSC_PATH, "svg_images"))
        icon = os.path.abspath(os.path.join(svg_image_folder, image_name))
        return icon

    # SET IMAGE
    def set_image(image_name):
        image_folder = os.path.abspath(os.path.join(IMG_RSC_PATH, "downloads"))
        image = os.path.abspath(os.path.join(image_folder, image_name))
        return image