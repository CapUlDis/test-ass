#!/bin/bash


psql -d $USER -c "CREATE DATABASE todoapp_devel"
psql -d $USER -c "CREATE DATABASE todoapp_test"

psql -d $USER -c "CREATE ROLE todoapp_user PASSWORD 'tdapp8' CREATEDB CREATEROLE LOGIN"
psql -d $USER -c "GRANT CREATE, CONNECT, TEMP ON DATABASE todoapp_devel, todoapp_test TO todoapp_user"

export TDA_DB=postgresql://todoapp_user:tdapp8@localhost/todoapp_devel 
alembic upgrade head
psql -d $TDA_DB -c "INSERT INTO users VALUES(1, 'denchik', 'pbkdf2:sha256:150000\$wHwsgiLd\$6979f267446c0e3d2797c21006f9272c3e19d5c70925d87989983ab3826350d8', 'foo@bar.baz');"

TDA_DB=postgresql://todoapp_user:tdapp8@localhost/todoapp_test alembic upgrade head