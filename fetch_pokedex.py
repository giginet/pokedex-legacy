# -*- coding: utf-8 -*-
#
# test.py
# created by giginet on 2013/10/21
#
import os
from pokedex.util.scraper import Scraper
if __name__ == '__main__':
    sc = Scraper()
    sc.fetch(os.path.join(os.getcwd(), 'dex'), interval=5.0)

