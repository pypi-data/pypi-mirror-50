# -*- coding: utf-8 -*-

name = 'gitlab'

version = '1.1.3'

def commands():
    global env
    global this
    global building
    
    for key, value in this._environ.items():
        env[key] = value

timestamp = 1564513198

_environ = {'GITLAB_URI': 'https://gitlab.mycompany.co.jp'}

format_version = 2
