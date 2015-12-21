# -*- coding: utf-8 -*-
import os
import etl2osm
import yaml
import json
import logging
from collections import OrderedDict


def ordered_load(stream, loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


class Models(object):
    """Models"""

    def __init__(self, path='', file_type='.yml'):
        self.container = {}
        self.__load(path, file_type)
        if len(self) == 0:
            logging.error('No Models Found - Verify <FILE PATH: {}> or <FILE TYPE: .yml .json>.'.format(path))

    def __load(self, path='', file_type='.yml'):
        print 'WARNING - Models {}'.format(path)
        # Try converting String to JSON dict
        # "{'foo': {'text': 'bar'}}"
        try:
            path = json.loads(path)
        except:
            pass

        if isinstance(path, self.__class__):
            self.container = path.container

        elif isinstance(path, dict):
            self.container['config'] = OrderedDict(path)
        else:
            # Look inside etl2osm [models] folder for .json files
            if not path:
                root = os.path.dirname(etl2osm.__file__)[:-len('etl2osm')]
                path = os.path.join(root, 'models')

            # Read Single File
            if os.path.isfile(path):
                with open(path) as f:
                    file_name = os.path.split(path)[-1]
                    self.container[os.path.splitext(file_name)[0]] = ordered_load(f, yaml.SafeLoader)

            # Read Entire Directory (Crawler)
            else:
                for root, dirs, files in os.walk(path):
                    for file_name in files:
                        if file_type in file_name:
                            with open(os.path.join(root, file_name)) as f:
                                self.container[os.path.splitext(file_name)[0]] = ordered_load(f, yaml.SafeLoader)

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
        if len(self) == 1:
            return '<etl2osm - Model [{}]>'.format(self.keys()[0])
        else:
            return '<etl2osm - Models [{}]>'.format(len(self))

    @property
    def config(self):
        if self:
            if len(self) == 1:
                return self.values()[0]
            else:
                return self.keys()


if __name__ == "__main__":
    # models = Models(OrderedDict([('hello', 'world'), ('foo', 'bar')]))
    # models = Models({'foo': 'bar'})
    models = Models('{"foo": "bar"}')
    print models.config
