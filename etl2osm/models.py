# -*- coding: utf-8 -*-
import os
import etl2osm
import yaml
import logging


class Models(object):
    """Models"""

    def __init__(self, path='', file_type='.yml'):
        self.container = {}
        self.load(path, file_type)
        if len(self) == 0:
            logging.error('No Models Found - Verify <FILE PATH: /models> or <FILE TYPE: .yml .json>.')

    def load(self, path='', file_type='.yml'):
        # Look inside etl2osm [models] folder for .json files
        if not path:
            root = os.path.dirname(etl2osm.__file__)[:-len('etl2osm')]
            path = os.path.join(root, 'models')

        for root, dirs, files in os.walk(path):
            for file_name in files:
                if file_type in file_name:
                    with open(os.path.join(root, file_name)) as f:
                        self.container[os.path.splitext(file_name)[0]] = yaml.load(f)

    def __getitem__(self, key):
        return self.container.get(key)

    def get(self, key):
        return self.container.get(key)

    def __setitem__(self, key, value):
        self.container[key] = value

    def __iter__(self):
        for item in self.container:
            yield item

    def __len__(self):
        return len(self.container)

    def items(self):
        return self.container.items()

    def keys(self):
        return self.container.keys()

    def values(self):
        return self.container.values()

    def __getattr__(self, key):
        if key not in self.container:
            error = "Models' object has no attribute '{}'".format(key)
            raise AttributeError(error)
        return self.container[key]

    def __repr__(self):
        return '<etl2osm - Models [{}]>'.format(len(self))


if __name__ == "__main__":
    model = Models()
