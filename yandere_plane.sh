#!/bin/bash

PROJECT_DIR=~/final-project-plane-KUROzeph
LOG_FILE=ai.log


gnome-terminal -- bash -c "
cd $PROJECT_DIR
touch $LOG_FILE
tail -f $LOG_FILE
exec bash
"

sleep 2

gnome-terminal -- bash -c "
cd $PROJECT_DIR
python3 main.py
exec bash
"