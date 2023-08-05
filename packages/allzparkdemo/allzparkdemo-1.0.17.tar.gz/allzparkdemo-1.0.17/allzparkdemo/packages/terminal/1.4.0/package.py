# -*- coding: utf-8 -*-

name = 'terminal'

version = '1.4.0'

requires = []

private_build_requires = ['rezutil-1']

def commands():
    global env
    
    env.PATH.append("{root}/bin")

timestamp = 1564501428

_data = {'icon': '{root}/resources/icon_128.png', 'label': 'Terminal'}

category = 'ext'

format_version = 2
