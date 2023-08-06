# -*- coding: utf-8 -*-

"""Top-level package for otzyvy.co."""

from .otzyvy_co import OtzyvyCo, Rating


__author__ = """NMelis"""
__email__ = 'melis.zhoroev+scrubbers@gmail.com'
__version__ = '0.1.1'
__title__ = 'otzyvy_co'
__description__ = 'OtzyvyCo'
__slug_img_link__ = 'https://i.ibb.co/cL7hyBL/image.png'
__how_get_slug = """
Slug это то что между https://otzyvy.co/company/ЭТОТ_SLUG/feedbacks/ без слешей (/)
<img src="{}" alt="image" border="0">
""".format(__slug_img_link__)


provider = OtzyvyCo
rating = Rating
