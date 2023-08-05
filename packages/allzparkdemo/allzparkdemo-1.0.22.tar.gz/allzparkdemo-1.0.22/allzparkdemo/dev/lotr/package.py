name = "lotr"
version = "1.13.4"

requires = [
    "base-1",

    # DCCs
    "~maya==2018.0.6|==2019.0.0",
    "~nuke==11.3.5",
]

build_command = "python -m rezutil build {root}"
private_build_requires = ["rezutil-1"]

_data = {
    "label": "Lord of the Rings",
    "icon": "{root}/resources/icon_{width}x{height}.png"
}
_environ = {
    "PROJECT_NAME": "Lord of the Rings",
    "PROJECT_PATH": "{env.PROJECTS_PATH}/lotr",

    # For locating in e.g. ftrack
    "PRODUCTION_TRACKER_ID": "lotr-124",
}


def commands():
    global env
    global this
    global expandvars

    for key, value in this._environ.items():
        if isinstance(value, (tuple, list)):
            [env[key].append(expandvars(v)) for v in value]
        else:
            env[key] = expandvars(value)
