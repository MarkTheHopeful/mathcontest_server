#!/usr/bin/env bash

export PYTHONPATH=$PYTHONPATH:"/home/mark/PycharmProjects/mathcontest_server:/home/mark/.local/share/JetBrains/Toolbox/apps/PyCharm-P/ch-0/202.6397.98/plugins/python/helpers/pycharm_matplotlib_backend:/home/mark/.local/share/JetBrains/Toolbox/apps/PyCharm-P/ch-0/202.6397.98/plugins/python/helpers/pycharm_display"
export MATHCONTEST_SERVER="http://34.69.97.127:5660"

python3 other_clients/http_client.py