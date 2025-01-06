import os
from configparser import Namespace
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, Union

import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script, ScriptDirectory

PROJECT_PATH = Path(__file__).parent.resolve()


def make_alembic_config(
    cmd_opts: Union[Namespace, SimpleNamespace], base_path: str = PROJECT_PATH
) -> Config:
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)

    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option(
            'script_location', os.path.join(base_path, alembic_location)
        )
    if cmd_opts.pg_url:
        config.set_main_option('sqlalchemy.url', cmd_opts.pg_url)

    return config


def alembic_config_from_url(pg_url: Optional[str] = None) -> Config:
    cmd_options = SimpleNamespace(
        config='alembic.ini',
        name='alembic',
        pg_url=pg_url,
        raiseerr=False,
        x=None,
    )

    return make_alembic_config(cmd_options)


def get_revisions():
    config = alembic_config_from_url()

    revisions_dir = ScriptDirectory.from_config(config)

    revisions = list(revisions_dir.walk_revisions('base', 'heads'))
    revisions.reverse()
    return revisions


@pytest.mark.parametrize('revision', get_revisions())
def test_migrations_stairway(alembic_config: Config, revision: Script):
    upgrade(alembic_config, revision.revision)

    downgrade(alembic_config, revision.down_revision or '-1')
    upgrade(alembic_config, revision.revision)
