#!/bin/bash


sudo -i -u postgres createdb todoapp_devel
sudo -i -u postgres createdb todoapp_test

sudo -i -u postgres createuser -s todoapp_user
