#!/bin/bash
printf %s 'ls -l src
whoami
uname -a
exit
' | script -q -e -c ./myshell /dev/null
