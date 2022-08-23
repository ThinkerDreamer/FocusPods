#! /usr/bin/env bash
# shellcheck source=/home/angel/focus-pods/FocusApp/.venv/bin/activate

source /home/angel/focus-pods/FocusApp/.venv/bin/activate
export DB_USERNAME="focus_pods"
export DB_PASSWORD="focus"
python3 -m server.focus_pods
