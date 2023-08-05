# -*- coding: utf-8 -*-

name = 'blender'

version = '2.80.0'

tools = ['blender']

requires = []

private_build_requires = ['rezutil-1']

def commands():
    global alias
    global system
    
    if system.platform == "windows":
        alias("blender", "notepad {root}/resources/readme.txt")
    else:
        # Making some assumptions here
        # TODO: Bullet proof this
        alias("blender", "gedit {root}/resources/readme.txt")

timestamp = 1564645146

_data = {'color': '#222', 'icon': '{root}/resources/icon_64.png', 'label': 'Blender'}

format_version = 2
