#!/usr/bin/env bash

# You should run this inside a tmux session

python3 base_server.py 2&> .base_server.log

# And then leave the session using ^-B d
# TODO: Make the whole server start process run using just one (this) script

