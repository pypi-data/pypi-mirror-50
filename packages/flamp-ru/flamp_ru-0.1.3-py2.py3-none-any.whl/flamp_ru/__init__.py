# -*- coding: utf-8 -*-

"""Top-level package for Flamp Ru."""
from flamp_ru.flamp_ru import FlampRU, Rating

__author__ = """NMelis"""
__email__ = 'melis.zhoroev@gmail.com'
__version__ = '0.1.3'
__name__ = 'Фламп ру'
__description__ = 'Отзывы о компаниях вашего города'
__slug_img_link__ = 'https://i.ibb.co/qdNzdNV/image.png'
__how_get_slug__ = """
Slug это цифры в конце url'а конкретной компании
<img src="{}" alt="image" border="0">

""".format(__slug_img_link__)

provider = FlampRU
rating = Rating
