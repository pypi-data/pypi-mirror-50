# -*- coding: utf-8 -*-

name = 'core_pipeline'

version = '1.1.1'

private_build_requires = ['rezutil-1']

def commands():
    global env
    global this
    global system
    global expandvars
    
    for key, value in this._environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)

timestamp = 1565007424

_environ = {'PYTHONPATH': ['{root}/python']}

format_version = 2
