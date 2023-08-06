import argparse
import importlib.util
import os.path
import sys
import os
import os.path
from mako.template import Template
import types

alias = {}
cache = {}
paths = {}

if os.path.exists(os.path.join(os.getcwd(), "./entrancebar.config.json")):
    try:
        import ujson as json
    except ModuleNotFoundError:
        import json
    context = json.load(open(os.path.join(os.getcwd(), "./entrancebar.config.json")))
    alias = context.get("alias", {})

def entrance_file(filename: str):
    for i in alias.keys():
        filename = filename.replace(i, alias[i])
    filename = Template(filename).render(projectDir=os.getcwd())
    path = os.path.join(os.path.dirname(os.path.abspath(sys._getframe(1).f_code.co_filename)), filename)
    if not cache.get(path):
        spec = importlib.util.spec_from_file_location(os.path.basename(path), path)
        origin = importlib.util.module_from_spec(spec)
        try:
            if path == sys._getframe(5).f_code.co_filename:
                return type(sys._getframe(5).f_globals['__name__'], (types.ModuleType,), sys._getframe(2).f_globals)
        except ValueError:
            pass
        loaded = spec.loader.exec_module(origin)
        cache[path] = {
            "origin": origin,
            "spec": spec,
            "enabled": True
        }
    else:
        if cache[path]['enabled']:
            origin = cache[path]["origin"]
        else:
            cache[path]['spec'].loader.exec_module(cache['origin'])
    return origin

def path_render(path):
    for i in alias.keys():
        path = path.replace(i, alias[i])
    path = Template(path).render(projectDir=os.getcwd(), **paths)
    return os.path.join(os.path.dirname(os.path.abspath(sys._getframe(1).f_code.co_filename)), path)

def add_path(key, path):
    paths[key] = path