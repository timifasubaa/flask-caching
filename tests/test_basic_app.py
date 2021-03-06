# -*- coding: utf-8 -*-
from flask import Flask
from flask_caching.backends.cache import SimpleCache
from flask_caching import Cache


class CustomSimpleCache(SimpleCache):
    pass


def newsimple(app, config, args, kwargs):
    return CustomSimpleCache(*args, **kwargs)


def test_dict_config(app):
    cache = Cache(config={'CACHE_TYPE': 'simple'})
    cache.init_app(app)

    assert cache.config['CACHE_TYPE'] == 'simple'


def test_dict_config_initapp(app):
    cache = Cache()
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    from flask_caching.backends.cache import SimpleCache
    assert isinstance(app.extensions['cache'][cache], SimpleCache)


def test_dict_config_both(app):
    cache = Cache(config={'CACHE_TYPE': 'null'})
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    from flask_caching.backends.cache import SimpleCache
    assert isinstance(app.extensions['cache'][cache], SimpleCache)


def test_init_app_sets_app_attribute(app):
    cache = Cache()
    cache.init_app(app)
    assert cache.app == app


def test_init_app_multi_apps(app):
    cache = Cache()
    app1 = Flask(__name__)
    app1.config.from_mapping(
        {
            'CACHE_TYPE': 'redis',
            'CACHE_KEY_PREFIX': 'foo'
        })

    app2 = Flask(__name__)
    app2.config.from_mapping(
        {
            'CACHE_TYPE': 'redis',
            'CACHE_KEY_PREFIX': 'bar'
        })
    cache.init_app(app1)
    cache.init_app(app2)

    # When we have the app context, the prefix should be
    # different for each app.
    with app1.app_context():
        assert cache.cache.key_prefix == 'foo'

    with app2.app_context():
        assert cache.cache.key_prefix == 'bar'


def test_app_custom_cache_backend(app):
    cache = Cache()
    app.config['CACHE_TYPE'] = 'test_basic_app.newsimple'
    cache.init_app(app)

    with app.app_context():
        assert isinstance(cache.cache, CustomSimpleCache)
