#!/bin/bash


psql -d $USER -c "CREATE DATABASE todoapp_devel"
psql -d $USER -c "CREATE DATABASE todoapp_test"

psql -d $USER -c "CREATE ROLE todoapp_user PASSWORD 'tdapp8' CREATEDB CREATEROLE LOGIN"
psql -d $USER -c "GRANT CREATE, CONNECT, TEMP ON DATABASE todoapp_devel, todoapp_test TO todoapp_user"

TDA_DB=postgresql://todoapp_user:tdapp8@localhost/todoapp_devel alembic upgrade head

TDA_DB=postgresql://todoapp_user:tdapp8@localhost/todoapp_test alembic upgrade head