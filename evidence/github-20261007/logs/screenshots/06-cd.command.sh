#!/bin/bash
printf %s 'pwd
cd /tmp
pwd
cd /not_exist
pwd
exit
' | script -q -e -c ./myshell /dev/null
