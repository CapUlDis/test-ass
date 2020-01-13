#!/bin/bash


createdb todoapp_devel
createdb todoapp_test

psql -c "CREATE ROLE todoapp_user PASSWORD 'tdapp8' CREATEDB CREATEROLE LOGIN"
psql -c "GRANT CREATE, CONNECT, TEMP ON DATABASE todoapp_devel, todoapp_test TO todoapp_user"
