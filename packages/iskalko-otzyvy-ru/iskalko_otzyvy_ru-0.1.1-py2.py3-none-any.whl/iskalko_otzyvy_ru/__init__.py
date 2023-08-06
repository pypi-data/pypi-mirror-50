# -*- coding: utf-8 -*-

"""Top-level package for iskalko_otzyvy_ru."""
from .iskalko_otzyvy_ru import IskalkoOtzyvyRu

__author__ = """Melis Nurlan"""
__email__ = 'melis.zhoroev+scrubber@gmail.com'
__version__ = '0.1.1'
__title__ = __name__ = 'Iskalko-Otzyvy.Ru'
__description__ = 'Каталог фирм, отзывы о компаниях'
__slug_img_link__ = 'https://i.ibb.co/VHmYq5w/image.png'
__how_get_slug__ = '''
Копируем заголовок/название страницы - это и будет slug
<img src="{}" alt="image" border="0">
'''.format(__slug_img_link__)


provider = IskalkoOtzyvyRu
