# -*- coding: utf-8 -*-

"""Top-level package for Rabota Otzyvy."""
from .rabotaotzyvy_ru import RabotaOtzyvyRu

__author__ = """NMelis"""
__email__ = 'melis.zhoroev+scrubbers@gmail.com'
__version__ = '0.1.6'
__title__ = __name__ = 'rabotaotzyvy.ru'
__description__ = 'Отзывы о работе, советы руководству'
__slug_img_link__ = 'https://i.ibb.co/Zh7KFbK/image.png'
__how_get_slug__ = """
Slug это то что между "https://rabotaotzyvy.ru/" и ".html"
<img src="{}" alt="image" border="0">
""".format(__slug_img_link__)

provider = RabotaOtzyvyRu
