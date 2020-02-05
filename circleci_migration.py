import os
import inspect as ins
from sqlalchemy import inspect, create_engine 
from alembic.config import Config
from alembic import command


os.environ['TDA_DB'] = 'postgresql://todoapp_user:tdapp8@localhost/todoapp_test'

this_file_directory = os.path.dirname(os.path.abspath(ins.stack()[0][1]))
root_directory      = os.path.join(this_file_directory, '..')
alembic_directory   = os.path.join(root_directory, 'alembic')
ini_path            = os.path.join(root_directory, 'alembic.ini')

alembic_cfg = Config(ini_path)
alembic_cfg.set_main_option('script_location', alembic_directory) 

command.upgrade(alembic_cfg, 'head')