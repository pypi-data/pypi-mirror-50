# -*- coding: utf-8 -*-
import os
from pathlib import Path

import pytest

from cenv_tool.project import Project
from cenv_tool.rules import RULES


def test_project_collect_available_envs():
    current_path = Path.cwd()
    testfolder = Path('tests/testproject')
    os.chdir(str(testfolder))
    project = Project(rules=RULES)
    os.chdir(str(current_path))
    available_envs = project.collect_available_envs()
    print(available_envs)


@pytest.mark.datafiles('tests/testproject')
def test_project_update(datafiles):
    created_env = Path('/shared/conda/envs/cenv_testing_project0001')
    environment_yml = Path(datafiles) / 'conda-build/environment.yml'
    current_folder = Path.cwd()
    os.chdir(datafiles)
    project = Project(rules=RULES)
    project.update()
    assert created_env.exists()
    project = Project(rules=RULES)
    project.update()
    assert created_env.exists()
    project = Project(rules=RULES)
    project.remove_previous_environment()
    project.remove_backup_environment()
    project.create_environment(cloned=False)
    project.export_environment_definition()
    assert environment_yml.exists()
    environment_yml.unlink()
    project.remove_previous_environment()
    project.remove_backup_environment()
    os.chdir(str(current_folder))
