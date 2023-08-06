# -*- coding: utf-8 -*-

name = 'maya_base'

version = '1.0.7'

requires = ['core_pipeline-2']

private_build_requires = ['rezutil-1']

def commands():
    global env
    global this
    global system
    global expandvars
    
    _environ = this._environ
    
    for key, value in _environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)

timestamp = 1565007417

_environ = \
    {'MAYA_DEBUG_SIGTERM_AS_SIGINT': '1',
     'MAYA_DISABLE_CER': '1',
     'MAYA_DISABLE_CIP': '1',
     'MAYA_DISABLE_CLIC_IPM': '1',
     'MAYA_ENABLE_LEGACY_VIEWPORT': '1',
     'MAYA_FORCE_PANEL_FOCUS': '0',
     'MAYA_PLUG_IN_PATH': ['{root}/maya/plugins'],
     'MAYA_RENDER_SETUP_INCLUDE_ALL_LIGHTS': '0',
     'MAYA_SCRIPT_PATH': ['{root}/maya/scripts'],
     'MAYA_VP2_DEVICE_OVERRIDE': 'VirtualDeviceDx11',
     'PYTHONPATH': ['{root}/maya/scripts', '{root}/maya/shelves'],
     'XBMLANGPATH': ['{root}/maya/shelves/icons']}

format_version = 2
