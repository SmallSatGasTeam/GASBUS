'''
This is the "discoverPlugins" plugin.

The discover plugins plugin goes through the plugins folder and looks for any new plugins that have been added. It then 
'''

from mainFlightLogic.plugins.plugin import Plugin

class DiscoverPlugins(Plugin):
    # TODO: discover all plugins in the plugins folder except plugin.py and log them in the database
    pass

        # module = __import__('plugins.heartbeat', fromlist=['Heartbeat'])
        # importClass = getattr(module, 'Heartbeat')

        # print(importClass)