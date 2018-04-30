#!/bin/bash
for file in ./test/correct/*.yal 
do
	python3 main.py $file
done
