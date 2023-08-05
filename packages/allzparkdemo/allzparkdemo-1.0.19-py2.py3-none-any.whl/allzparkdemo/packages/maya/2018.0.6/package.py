# -*- coding: utf-8 -*-

name = 'maya'

version = '2018.0.6'

tools = [
    'maya',
    'mayapy',
    'render',
    'mayabatch'
]

requires = []

private_build_requires = ['rezutil-1']

def commands():
    import os
    
    global this
    global env
    global alias
    global system
    
    exes = ["maya", "mayapy", "mayabatch", "render"]
    ext = ""
    version = "2018"
    print(this.version, type(this.version))
    
    # Edit these to support more versions of Maya
    if os.name == "nt":
        bindir = r"c:\program files\autodesk\maya{}\bin".format(version)
        ext = ".exe"
    elif os.name == "posix":
        bindir = "Unknown"
    elif os.name == "darwin":
        bindir = "Unknown"
    else:
        bindir = "Unknown"
    
    if os.path.exists(bindir):
        for exe in exes:
            alias(exe, os.path.join(bindir, exe + ext))
    
    else:
        if system.platform == "windows":
            alias("maya", "notepad {root}/resources/readme.txt")
        else:
            # Making some assumptions here
            # TODO: Bullet proof this
            alias("maya", "gedit {root}/resources/readme.txt")

timestamp = 1564513199

_data = \
    {'color': '#251',
     'icon': '{root}/resources/icon_256x256.png',
     'label': 'Autodesk Maya'}

format_version = 2
