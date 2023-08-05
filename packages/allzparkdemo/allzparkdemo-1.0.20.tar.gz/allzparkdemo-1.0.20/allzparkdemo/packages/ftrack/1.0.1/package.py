# -*- coding: utf-8 -*-

name = 'ftrack'

version = '1.0.1'

def commands():
    global env
    global this
    global building
    
    for key, value in this._environ.items():
        env[key] = value

timestamp = 1564645140

_environ = {'FTRACK_PROTOCOL': 'https', 'FTRACK_URI': 'ftrack.mystudio.co.jp'}

format_version = 2
