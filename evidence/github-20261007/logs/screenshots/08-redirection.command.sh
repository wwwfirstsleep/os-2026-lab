#!/bin/bash
printf %s 'echo hello > screenshot-out.txt
echo world >> screenshot-out.txt
cat < screenshot-out.txt
cat screenshot-out.txt
exit
' | script -q -e -c ./myshell /dev/null
