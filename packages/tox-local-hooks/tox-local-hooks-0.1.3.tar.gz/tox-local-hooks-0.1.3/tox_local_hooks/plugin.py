import importlib.util
import sys
import os
import tox.config
import traceback


def get_tox_conffile():
    parser = tox.config.Parser()
    tox.config.tox_addoption(parser)
    option, _ = parser.argparser.parse_known_args(sys.argv)
    for f in tox.config.propose_configs(option.configfile):
        conf_file = f
    return conf_file


def get_hooks_file():
    return os.path.abspath(get_tox_conffile().dirname) + '/toxhooks.py'


def load_hooks_file():
    hooks_file = get_hooks_file()
    if not os.path.isfile(hooks_file):
        return
    try:
        spec = importlib.util.spec_from_file_location("toxhooks", hooks_file)
        hook = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hook)
        for attr in dir(hook):
            if attr.startswith('tox_'):
                globals()[attr] = getattr(hook, attr)
    except Exception:
        traceback.print_exc()
        pass


load_hooks_file()
