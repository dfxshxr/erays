#!/bin/bash

python graphbuilder.py temp/temp2.hex -d > 0.1.graphbuilder.txt
python lifter.py temp/temp2.hex -d > 0.2.lifter.txt
python optimizer.py temp/temp2.hex -d > 0.3.optimizer.txt
python aggregator.py temp/temp2.hex -d > 0.4.aggregator.txt
python structurer.py temp/temp2.hex -d > 0.5.structurer.txt
