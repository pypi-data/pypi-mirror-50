#!/usr/bin/env python3
# coding: utf-8

import os.path

import yaml

__version__ = '0.1'
_conf = None


def _load_conf():
    from joker.default import under_home_dir
    paths = [under_home_dir('.m14-default.yml'), '/etc/m14-default.yml']
    for path in paths:
        if os.path.isfile(path):
            return yaml.safe_load(open(path))


def _get_conf():
    global _conf
    if _conf is None:
        _conf = _load_conf() or {}
    return _conf


def under_default_dir(package, *paths):
    conf = _get_conf()
    name = getattr(package, '__name__', str(package)).split('.')[-1]
    try:
        dir_ = conf[name]
    except LookupError:
        dir_ = os.path.join(conf.get('default', '/data'), name)
    return os.path.join(dir_, *paths)
