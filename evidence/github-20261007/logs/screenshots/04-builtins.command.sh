#!/bin/bash
printf %s 'pwd
echo hello
echo $HOME
echo $PATH
exit
' | script -q -e -c ./myshell /dev/null
