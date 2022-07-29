'''
This is the "startup" plugin.

The startup plugin is run when the satellite starts up. It is the first task and schedules all the other tasks that should run immediately after the satellite starts.
'''

from plugins.plugin import Plugin
from objects.log import Log

class Startup(Plugin):
    def __init__(self, pluginId, identifier, pluginParameters):
        super().__init__(pluginId, identifier)

    @classmethod
    def newPlugin(cls, runTaskId, runPluginId):
        return super().newPlugin(cls, 'startup', [], runTaskId, runPluginId)
