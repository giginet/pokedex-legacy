# -*- coding: utf-8 -*-
import urllib2
import urlparse
import time

import re
import lxml
from lxml.html import fromstring

from pokedex.pokemon import Pokemon

class Scraper(object):

    SOURCE_URL = r'http://wiki.gamerp.jp/pokemon/data/330.html'

    def __init__(self):
        html = urllib2.urlopen(self.SOURCE_URL)
        dom = fromstring(html.read())
        trs = dom.cssselect('div#data2 table tr')
        def get_urls(tr_element):
            no, name = list(tr_element)
            no = no.text.strip()
            if no.isdigit():
                url = list(name)[0].attrib['href']
                name = list(name)[0].text
                return (no, name, url)
            return None
        self.infos = filter(lambda p: p, [get_urls(tr) for tr in trs])

    def fetch(self, output_dir, interval=1.0):
        for info in self.infos:
            pokemon = self._parse_pokemon(info)
            print "%d %s parsed" % (pokemon.number, pokemon.name)
            time.sleep(interval)
            pokemon.save_json(output_dir)

    def _parse_pokemon(self, info):
        no, name, url = info
        url = urlparse.urljoin(self.SOURCE_URL, url)
        html = urllib2.urlopen(url)
        dom = fromstring(html.read())
        pokemon = Pokemon(no, name, url)

        tables = dom.cssselect('table.pokemon_table table')

        index = 1
        # species
        try:
            about = tables[0].cssselect('tr')[index][0].text_content().strip()
            m = re.search(r'\D+$', about, re.UNICODE)
            pokemon.species = m.group(0)
        except:
            pokemon.species = ''

        try:
            image_url = tables[0].cssselect('tr')[index][1].cssselect('img')[0].attrib['src']
            pokemon.image_url = image_url
        except:
            pokemon.image_url = ''

        # types
        try:
            index += 1
            types = tables[0].cssselect('tr')[index].cssselect('td td')
            pokemon.types = map(lambda type_element: type_element.text, types)
        except:
            pokemon.types = []

        # egg group
        try:
            index += 2
            egg_groups = tables[0].cssselect('tr')[index][1].text_content().split('/')
            pokemon.egg_groups = map(lambda egg_group: egg_group.strip(), egg_groups)
        except:
            pokemon.egg_groups = []

        # height, weight
        try:
            index += 2
            height, weight = tables[0].cssselect('tr')[index][1].text_content().split('/')
            pokemon.height = float(re.search(r'[\d\.]+', height.strip()).group(0))
            pokemon.weight = float(re.search(r'[\d\.]+', weight.strip()).group(0))
        except:
            pokemon.height = 0
            pokemon.weight = 0

        # friendship
        try:
            index += 1
            pokemon.friendship = int(tables[0].cssselect('tr')[index][1].text)
        except:
            pokemon.friendship = 0

        # exp
        try:
            index += 1
            pokemon.exp = int(tables[0].cssselect('tr')[index][1].text)
        except:
            pokemon.exp = 0

        # parameters
        keys = ['hp', 'attack', 'block', 'critical', 'defense', 'speed', 'total']
        parameters = {}
        try:
            trs = tables[2].cssselect('tr')
            for i, key in enumerate(keys):
                n = trs[1 + i][1].text
                parameters[key] = int(n)
        except:
            for key in keys:
                parameters[key] = 0
        pokemon.parameters = parameters

        # abilities
        try:
            table = dom.cssselect("table.pokemon_table + table")
            trs = table[0].cssselect('tr')
            pokemon.abilities = [tr[1].cssselect('a')[0].text for tr in trs if u"特性" in tr[0].text]
        except:
            pokemon.abilities = []

        return pokemon

if __name__ == '__main__':
    sc = Scraper()
