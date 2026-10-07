#!/bin/bash
printf %s 'ls | wc -l
printf hello | wc -c
cat screenshot-out.txt | wc -w
exit
' | script -q -e -c ./myshell /dev/null
