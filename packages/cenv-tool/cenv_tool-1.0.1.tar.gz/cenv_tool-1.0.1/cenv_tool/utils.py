# -*- coding: utf-8 -*-
"""Contain utils required by cenv-tool."""
import os
from pathlib import Path
from subprocess import CalledProcessError
from subprocess import check_output
from subprocess import STDOUT
from typing import NoReturn

import jinja2
import six
from marshmallow import ValidationError
from ruamel.yaml import YAML

from cenv_tool.schemata import SMetaYaml

CYAN = '\033[1;36m'
GREEN = '\033[1;32m'
RED = '\033[1;91m'
NCOLOR = '\033[0m'
BOLD = '\033[1;37m'


class CenvProcessError(Exception):
    """Represent a process error during cenv execution."""


def message(
    *, text: str, color: str, special: str = None, indent: int = 1
) -> NoReturn:
    """Print the passed text in the passed color on terminal.

    Parameters:
        text: The text to print colored on terminal

    """
    color_mapping = {
        'red': RED,
        'green': GREEN,
        'cyan': CYAN,
        'bold': BOLD,
    }
    if indent == 1:
        indent_prefix = '   ' * indent
    else:
        indent_prefix = '   ' + '│   ' * (indent - 1)
    special_mapping = {
        'row': f'{indent_prefix}├── ',
        'end': f'{indent_prefix}└── ',
    }

    if special:
        prefix = special_mapping[special]
    else:
        prefix = ''
    print(f'{prefix}{color_mapping[color]}{text}{NCOLOR}')


def run_in_bash(cmd: str) -> str:
    """Run passed cmd inside bash using the subprocess.check_output-function.

    Parameters:
        cmd: the command to execute.

    Returns:
        the output of the ran command.

    """
    try:
        result = check_output([cmd], shell=True, stderr=STDOUT)
    except CalledProcessError:
        raise CenvProcessError()
    return result.strip().decode('ascii')


class NullUndefined(jinja2.Undefined):
    """Handle jinja2-variables with undefined content inside the meta.yaml."""

    def __unicode__(self):
        """Replace uncode dunder of this class."""
        return six.text_type(self._undefined_name)

    def __getattr__(self, attribute_name: str):
        """Replace getattr dunder of this class."""
        return six.text_type(f'{self}.{attribute_name}')

    def __getitem__(self, attribute_name: str):
        """Replace getitem dunder of this class."""
        return f'{self}["{attribute_name}"]'


class StrDict(dict):
    """Handle dictionaries for jinja2-variables inside the meta.yaml."""

    def __getitem__(self, key: str, default: str = '') -> str:
        """Replace getitem dunder of this class."""
        return self[key] if key in self else default


def read_meta_yaml(path: Path) -> dict:
    """Read the meta.yaml file.

    The file is read from relative path conda-build/meta.yaml inside
    the current path, validates the meta.yaml using the marshmallow-schema,
    extracts the dependency-information and the project-settings and returns
    these information.

    Parameters:
        path: The current working directory

    Returns:
        List containing the project-settings as a dict and the dependencies
        also as a dict

    """
    # load the meta.yaml-content
    myaml_content = (path / 'conda-build/meta.yaml').open().read()
    jinja2_env = jinja2.Environment(undefined=NullUndefined)
    jinja2_loaded_myaml = jinja2_env.from_string(myaml_content)
    render_kwargs = {
        'os': os,
        'environ': StrDict(),
        'load_setup_py_data': StrDict,
    }
    rendered_myaml = jinja2_loaded_myaml.render(**render_kwargs)
    loaded_myaml = YAML(typ='base').load(rendered_myaml)

    # validate the content of loaded meta.yaml
    try:
        dumped = SMetaYaml(strict=True).dumps(loaded_myaml).data
        meta_yaml_content = SMetaYaml(strict=True).loads(dumped).data
    except ValidationError as err:
        message(text='meta.yaml file is not valid!', color='red')
        message(text=f'ValidationError in {err.args[0]}', color='red')
        raise

    # extract the dependencies defined the the requirements-run-section
    dependencies = meta_yaml_content['requirements']['run']
    if meta_yaml_content['extra'].get('dev_requirements'):
        dependencies.extend(meta_yaml_content['extra']['dev_requirements'])

    # combine the collected project-settings and the collected dependencies
    # to one output of this function
    return meta_yaml_content, dependencies


def read_config():
    """Read the config file for cenv from the users-home path if it exists.

    If there is no user-config-file the default one is used.

    Returns:
        the content of the read config file.

    """
    user_config_path = Path.home() / '.config/cenv/cenv.yml'
    default_config_path = Path(__file__).parent / 'cenv.yml'

    # Collect settings from config file .cenv.yml
    main_config = YAML(typ='safe').load(default_config_path.open().read())

    # if a user-config-file exists, read the content and update the main-config
    if user_config_path.exists():
        user_config = YAML(typ='safe').load(user_config_path.open().read())
        main_config.update(user_config)

    return main_config
