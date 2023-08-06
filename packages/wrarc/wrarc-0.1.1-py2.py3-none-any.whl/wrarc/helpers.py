import json
import yaml


def unicode_to_str(u):
    return u.encode('ascii', 'ignore')


def clean_string(s):
    return s.strip().replace(' ', '')


def get_comma_delimitted_list(s):
    return s.split(',')


def get_phab_cli(ctx):
    return ctx.obj['phabricator']


def load_json_from_file(f):
    return json.load(f)


def load_yaml_from_file(f):
    return yaml.safe_load(f)
