#!/usr/bin/env bash

export PYTHONPATH=$PYTHONPATH:"~/PycharmProjects/mathcontest_server:~/.local/share/JetBrains/Toolbox/apps/PyCharm-P/ch-0/202.6397.98/plugins/python/helpers/pycharm_matplotlib_backend:~.local/share/JetBrains/Toolbox/apps/PyCharm-P/ch-0/202.6397.98/plugins/python/helpers/pycharm_display" # FIXME: won't work on 99% other machines
export MATHCONTEST_SERVER="http://34.69.97.127:5660"

python3 other_clients/http_client.py