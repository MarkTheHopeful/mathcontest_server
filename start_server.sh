#!/usr/bin/env bash

# You should run this inside a tmux session

export FLASK_APP=mathcontest_server.py
flask run 2&> .mathcontest_server.log

# And then leave the session using ^-B d
# TODO: Make the whole app start process run using just one (this) script
