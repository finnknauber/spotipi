#!/bin/bash

cd /home/pi/spotipi

touch output.log
 
nohup sudo python main.py >> output.log 2>> output.log &
