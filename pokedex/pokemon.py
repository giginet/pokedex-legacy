import json
import os
import codecs

class Pokemon(object):

    def __init__(self, number, name, url):
        self.url = url
        self.number = int(number)
        self.name = name
        self.species = ''
        self.types = []
        self.abilities = []
        self.weight = 0
        self.height = 0
        self.egg_groups = []
        self.image_url = ''
        self.exp = 0
        self.friendship = 0
        self.parameters = {}

    def to_dict(self):
        return {
            'name' : self.name,
            'number' : self.number,
            'species' : self.species,
            'types' : self.types,
            'egg_groups' : self.egg_groups,
            'height' : self.height,
            'weight' : self.weight,
            'friendship' : self.friendship,
            'exp' : self.exp,
            'abilities' : self.abilities,
            'parameters' : self.parameters,
            'image_url' : self.image_url
        }

    def save_json(self, dirpath):
        # Ref http://d.hatena.ne.jp/tatz_tsuchiya/20120227/1330325015
        data = self.to_dict()
        f = codecs.open(os.path.join(dirpath, "dex%d.json" % self.number), 'w', 'utf-8')
        json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.close()
