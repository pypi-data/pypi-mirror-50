# -*- coding: utf-8 -*-

name = 'houdini'

version = 'fx.17.5.1'

tools = [
    'houdini',
    'houdinifx'
]

requires = []

private_build_requires = ['rezutil-1']

def commands():
    import os
    global env
    global alias
    global system
    
    if system.platform == "windows":
        bindir = "c:\\windows\\system32"
    
    elif system.platform == "linux":
        bindir = "/opt/nuke11.3v3/bin/"
    
    if not os.path.exists(bindir):
        print("WARNING: Missing files: %s" % bindir)
    
    bindir = "\"%s\"" % bindir
    
    # Add specific names to executables made
    # available by this package.
    alias("nuke", "notepad")

timestamp = 1564501428

_data = \
    {'icons': {'32x32': '{root}/resources/icon_256x256.png',
               '64x64': '{root}/resources/icon_256x256.png'}}

format_version = 2
