import os.path
import json
from ruamel.yaml import YAML

yaml = YAML(typ="safe")
yaml.default_flow_style = False

from .dotenv import parser as dotenv_parser


def parse_file(env_file):
    path, ext = os.path.splitext(env_file)
    if ext == ".yaml":
        return read_yaml(env_file)
    if ext == ".json":
        return read_json(env_file)
    if ext == ".env" or os.path.basename(path) == ".env":
        return read_env(env_file)
    raise ValueError("Unknown environment variable file type: %s" % (env_file,))


def read_yaml(fname):
    data = {}
    with open(fname, "r") as f:
        data = yaml.load(f)
    return data


def read_json(fname):
    data = {}
    with open(fname, "r") as f:
        data = json.load(f)
    return data


def read_env(fname):
    data = {}
    with open(fname, "r") as f:
        for mapping in dotenv_parser.parse_stream(f):
            if mapping.key is not None and mapping.value is not None:
                data[mapping.key] = mapping.value
    return data
