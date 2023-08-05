# -*- coding: utf-8 -*-

name = 'default_project'

version = '1.0.1'

requires = ['python']

private_build_requires = ['rezutil-1']

def commands():
    global env
    global alias
    
    # For Windows
    env.PATH.prepend("{root}/bin")
    
    # For Unix
    alias("create", "python {root}/bin/create.py")

timestamp = 1564501429

category = 'int'

format_version = 2
