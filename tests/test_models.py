# -*- coding: utf-8 -*-

from etl2osm import Models


def test_models_len():
    models = Models()
    assert len(models)
    empty = Models('/blank-path')
    assert not len(empty)


def test_models_in():
    models = Models()
    assert 'direction' in models
    assert 'not exist' not in models


def test_models_get():
    models = Models()
    assert models.get('direction')
    assert models.direction
    assert models['direction']


def test_models_set():
    models = Models()
    models['direction'] = {'foo': 'bar'}
    assert models['direction'] == {'foo': 'bar'}


def test_models_items():
    models = Models()
    assert models.items()
    assert models.values()
    assert models.keys()


def test_models_for():
    models = Models()
    for item in models:
        assert item


def test_models_inherent():
    assert Models().config
    assert Models({'foo': 'bar'}).config
    assert Models(Models({'foo': 'bar'})).config
    assert Models('{"foo": "bar"}').config


if __name__ == '__main__':
    test_models_inherent()
