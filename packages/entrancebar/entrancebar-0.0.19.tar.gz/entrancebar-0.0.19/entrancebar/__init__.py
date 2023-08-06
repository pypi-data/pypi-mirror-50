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

packages = {}

def path_render(path):
    for i in alias.keys():
        path = path.replace(i, alias[i])
    path = Template(path).render(projectDir=os.getcwd(), **paths)
    return os.path.join(os.path.dirname(os.path.abspath(sys._getframe(1).f_code.co_filename)), path)

def entrance_file(filename: str):
    for i in alias.keys():
        filename = filename.replace(i, alias[i])
    filename = Template(filename).render(projectDir=os.getcwd(), **paths)
    path = os.path.join(os.path.dirname(os.path.abspath(sys._getframe(1).f_code.co_filename)), filename)
    if not cache.get(path):

        if os.path.isdir(path):
            if os.path.exists(os.path.join(path, "./__init__.py")):
                spec = importlib.util.spec_from_file_location(
                    os.path.basename(os.path.dirname(path)),
                    os.path.join(path, "./__init__.py")
                )
            elif os.path.exists(os.path.join(path, "./main.py")):
                spec = importlib.util.spec_from_file_location(
                    os.path.basename(os.path.dirname(path)),
                    os.path.join(path, "./main.py")
                )
            elif os.path.exists(os.path.join(path, "./index.py")):
                spec = importlib.util.spec_from_file_location(
                    os.path.basename(os.path.dirname(path)),
                    os.path.join(path, "./index.py")
                )
            elif os.path.exists(os.path.join(path, "./entry.py")):
                spec = importlib.util.spec_from_file_location(
                    os.path.basename(os.path.dirname(path)),
                    os.path.join(path, "./entry.py")
                )
            else:
                spec = importlib.util.spec_from_file_location(
                    os.path.basename(os.path.dirname(path)),
                    "NOTFOUNDER!~@#$%^&*()"
                )
        else:
            spec = importlib.util.spec_from_file_location(os.path.basename(path), path)
        origin = importlib.util.module_from_spec(spec)
        
        if sys._getframe(1).f_globals['__name__'] == "__main__":
            cache[os.path.abspath(sys._getframe(1).f_code.co_filename)] = {
                "origin": type("RunningProgram", (types.ModuleType,), sys._getframe(1).f_globals),
                "enabled": True,
                "spec": None
            }

        # 避免爆栈, 并且实现了相互调用
        n = 1
        while True:
            try:
                if path == sys._getframe(n).f_code.co_filename:
                    return type(sys._getframe(n).f_globals['__name__'], (types.ModuleType,), sys._getframe(n).f_globals)
            except ValueError:
                break
            n += 4

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

class PackageType:
    @staticmethod
    def SingleFile(path):
        return entrance_file(path)

    @staticmethod
    def Line(path):
        class Defaultify(object):
            def __getattr__(self, value: str = ""):
                if value.startswith("__") and value.endswith("__"):
                    return super().__getattr__(value)
                if not value:
                    value = "default"
                return self.path[value]

            def __setattr__(self, value):
                raise ValueError("Cannot able to call the method.")
        
        return type("method", (Defaultify,), {
            "path": {
                "default": entrance_file(path[-1])
            } + {i: entrance_file(i) for i in path[:-1]}
        })

def entrance_package(package):
    if not packages.get(package):
        raise ImportError(f"Cannot able to find package '{package}'")
    context = packages[package]
    return getattr(PackageType(), context['type'])(path=context['path'])

if os.path.exists(os.path.join(os.getcwd(), "./entrancebar.config.json")):
    try:
        import ujson as json
    except ModuleNotFoundError:
        import json
    context = json.load(open(os.path.join(os.getcwd(), "./entrancebar.config.json")))
    alias = context.get("alias", {})
    if context.get("global"):
        if context['global'].get("packages"):
            for key, value in context['global']["packages"].items():
                if isinstance(value, str):
                    packages[key] = {
                        "type": "SingleFile",
                        "path": path_render(value)
                    }
                elif isinstance(value, list):
                    packages[key] = {
                        "type": "Line",
                        "path": [path_render(i) for i in value]
                    }
                else:
                    raise TypeError(f"Unknown package type '{key}'")