'''
This is the "startup" plugin.

The startup plugin is run when the satellite starts up. It is the first task and schedules all the other tasks that should run immediately after the satellite starts.
'''

from mainFlightLogic.plugins.plugin import Plugin

class Startup(Plugin):
    pass