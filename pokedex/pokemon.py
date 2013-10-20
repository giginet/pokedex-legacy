import json
import os

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
            'parameters' : self.parameters
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def save_json(self, dirpath):
        json_string = self.to_json()
        cwd = os.getcwd()
        f = open(os.path.join(cwd, dirpath, "dex%d.json" % self.number), 'w')
        f.write(json_string)
        f.close()
