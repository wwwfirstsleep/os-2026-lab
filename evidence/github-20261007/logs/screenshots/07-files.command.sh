#!/bin/bash
printf %s 'touch screenshot-demo.txt
echo data > screenshot-demo.txt
cat screenshot-demo.txt
rm screenshot-demo.txt
cat screenshot-demo.txt
echo alive
exit
' | script -q -e -c ./myshell /dev/null
