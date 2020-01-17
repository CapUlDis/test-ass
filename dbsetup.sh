#!/bin/bash


createdb todoapp_devel
createdb todoapp_test

psql -c "CREATE ROLE todoapp_user PASSWORD 'tdapp8' CREATEDB CREATEROLE LOGIN"
psql -c "GRANT CREATE, CONNECT, TEMP ON DATABASE todoapp_devel, todoapp_test TO todoapp_user"
psql -d todoapp_test -c "INSERT INTO users VALUES(1, 'denchik', 'pbkdf2:sha256:150000\$wHwsgiLd\$6979f267446c0e3d2797c21006f9272c3e19d5c70925d87989983ab3826350d8', 'capuldis@gmail.com')"
