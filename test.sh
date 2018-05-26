#!/bin/bash
for file in ./test/*/*.yal 
do
	python3 main.py $file
done
