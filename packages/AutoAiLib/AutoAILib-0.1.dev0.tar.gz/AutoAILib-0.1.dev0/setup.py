# -*- coding: utf-8 -*-
from setuptools import setup, Extension
from bs4 import BeautifulSoup as soup
from markdown import markdown
description = markdown(open('README.md').read())
#text = ''.join(soup(description, 'lxml').findAll(text=True))
setup(name="AutoAILib",
      version ='0.1dev',
      packages=['AutoAILib',],
      license='GNU GPLv3',
      long_description=description,
      long_description_content_type = 'text/markdown')