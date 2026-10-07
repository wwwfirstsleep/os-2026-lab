#!/bin/bash
printf %s 'echo OS-LAB1-started
exit
' | script -q -e -c ./myshell /dev/null
