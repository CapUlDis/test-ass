import pytest, os
import inspect as ins
from sqlalchemy import inspect, create_engine 
from alembic.config import Config
from alembic import command
from flask import current_app
from models import User


this_file_directory = os.path.dirname(os.path.abspath(ins.stack()[0][1]))
root_directory      = os.path.join(this_file_directory, '..')
alembic_directory   = os.path.join(root_directory, 'alembic')
ini_path            = os.path.join(root_directory, 'alembic.ini')

alembic_cfg = Config(ini_path)
alembic_cfg.set_main_option('script_location', alembic_directory) 

def test_alembic_downgrade_upgrade_migrations(app):
    command.downgrade(alembic_cfg, 'base')
    with app.app_context():
        insp_1 = inspect(current_app.engine)
        assert 'users' not in insp_1.get_table_names()
        command.upgrade(alembic_cfg, 'head')
        insp_2 = inspect(current_app.engine)
        recieved_names_of_columns = [column['name'] for column in insp_2.get_columns('users')]
        assert 'users' in insp_2.get_table_names()
        assert User().__table__.columns.keys() == recieved_names_of_columns