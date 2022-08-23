#! /usr/bin/env bash

unshare --pid --fork --mount-proc /lib/systemd/systemd --system-unit=basic.target &
sleep 5
nsenter --all -t "$(pgrep -xo systemd)" runuser -P -l "$USER" -c "exec $SHELL"
systemctl start postgresql.service