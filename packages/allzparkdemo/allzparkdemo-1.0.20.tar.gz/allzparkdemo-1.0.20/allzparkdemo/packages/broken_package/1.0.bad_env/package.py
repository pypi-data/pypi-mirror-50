# -*- coding: utf-8 -*-

name = 'broken_package'

version = '1.0.bad_env'

def commands():
    global env
    
    # This throws an error
    env["BAD"] = "{env.NOT_EXIST}"

timestamp = 1564645142

format_version = 2
