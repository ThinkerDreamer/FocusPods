#! /usr/bin/env bash

# This starts postgres on Ubuntu over Windows Subsystem for Linux, on my machine anyway.
unshare --pid --fork --mount-proc /lib/systemd/systemd --system-unit=basic.target &
sleep 5
nsenter --all -t "$(pgrep -xo systemd)" runuser -P -l "$USER" -c "exec $SHELL"
systemctl start postgresql.service
