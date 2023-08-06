# -*- coding: utf-8 -*-

"""Top-level package for  bad_otzyvy_net."""
from .bad_otzyvy_net import _StatusReview, BadOtzyvyNet, Rating

__author__ = """NMelis"""
__email__ = 'melis.zhoroev+scrubbers@gmail.com'
__version__ = '0.1.2'
__title__ = __name__ = 'bad-otzyvy.net'
__description__ = 'Bad-Good: Отзывы о компаниях'
__slug_img_link__ = 'https://i.ibb.co/9WyqSk0/image.png'
__how_get_slug__ = """
Slug это то что между "https://bad-otzyvy.net/" и ".html"
<img src="{}" alt="image" border="0">
""".format(__slug_img_link__)

provider = BadOtzyvyNet
rating = Rating
status = _StatusReview
