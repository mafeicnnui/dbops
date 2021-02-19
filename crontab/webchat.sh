#!/usr/bin/env bash
export PYTHON3_HOME=/home/hopson/apps/usr/webserver/dba/python3.6.0
export LD_LIBRARY_PATH=$PYTHON3_HOME/lib
export SCRIPT_PATH=/home/hopson/apps/usr/webserver/dba/syncer/dba_monitor
$PYTHON3_HOME/bin/python3 $SCRIPT_PATH/webchat.py >$SCRIPT_PATH/webchat.log &
