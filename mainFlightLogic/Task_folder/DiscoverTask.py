import importlib
import pkgutil
import sys

def getTasks():
    discovered_plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules()
        if name.startswith('Task_')
    }
    print(discovered_plugins)
    return discovered_plugins