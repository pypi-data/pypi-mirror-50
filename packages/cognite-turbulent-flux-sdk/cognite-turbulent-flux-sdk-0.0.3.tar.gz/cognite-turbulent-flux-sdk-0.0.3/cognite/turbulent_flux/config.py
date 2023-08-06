import re
from typing import *
import yaml
import os
path = os.path.dirname(os.path.abspath(__file__))
config_parsed = yaml.safe_load(open(path + '/config.yml'))


# Format all strings in config
def format_tree(tree):
    if type(tree) is dict:
        for key, val in tree.items():
            tree[key] = format_tree(val)
        return tree
    if type(tree) is list:
        for i, val in enumerate(tree):
            tree[i] = format_tree(val)
        return tree
    if type(tree) is str:
        return tree.format(**config_parsed)

config_parsed = format_tree(config_parsed)

locals().update(config_parsed)

urls: Dict[str, str]
