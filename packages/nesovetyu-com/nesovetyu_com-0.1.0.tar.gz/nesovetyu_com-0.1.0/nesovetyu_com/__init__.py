# -*- coding: utf-8 -*-

"""Top-level package for nesovetyu_com."""
from .nesovetyu_com import Rating, NesovetyuCom

__author__ = """NMelis"""
__email__ = 'melis.zhoroev+scrubbers@gmail.com'
__version__ = '0.1.0'
__name__ = __title__ = 'nesovetyu.com'
__slug_img_link__ = 'https://i.ibb.co/Yjf69bH/image.png'
__description__ = 'nesovetyu.com'
__how_get_slug__ = """
Slug это то что между "https://nesovetyu.com/" и ".html"
<img src="{}" alt="image" border="0">
""".format(__slug_img_link__)


provider = NesovetyuCom
rating = Rating

