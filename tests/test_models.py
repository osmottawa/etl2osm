# -*- coding: utf-8 -*-

from etl2osm import Models

models = Models()


def test_models_len():
    assert len(models)
    empty = Models('/blank-path')
    assert not len(empty)


def test_models_in():
    assert 'direction' in models
    assert 'not exist' not in models


def test_models_get():
    assert models.get('direction')
    assert models.direction
    assert models['direction']


def test_models_set():
    models['direction'] = {'foo': 'bar'}
    assert models['direction'] == {'foo': 'bar'}


def test_models_items():
    assert models.items()
    assert models.values()
    assert models.keys()


def test_models_for():
    for item in models:
        assert item

if __name__ == '__main__':
    test_models_len()
