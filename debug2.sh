#!/bin/bash

python disassembler.py temp/0xba2ed0d772e0ca1f72368e7a610e42397e960946.hex -d > 2.0.disassembler.txt
python graphbuilder.py temp/0xba2ed0d772e0ca1f72368e7a610e42397e960946.hex -d > 2.1.graphbuilder.txt
python lifter.py temp/0xba2ed0d772e0ca1f72368e7a610e42397e960946.hex -d > 2.2.lifter.txt
python optimizer.py temp/0xba2ed0d772e0ca1f72368e7a610e42397e960946.hex -d > 2.3.optimizer.txt
python aggregator.py temp/0xba2ed0d772e0ca1f72368e7a610e42397e960946.hex -d > 2.4.aggregator.txt
python structurer.py temp/0xba2ed0d772e0ca1f72368e7a610e42397e960946.hex -d > 2.5.structurer.txt

python graphbuilder.py temp/0xba2ed0d772e0ca1f72368e7a610e42397e960946.hex -v
python lifter.py temp/0xba2ed0d772e0ca1f72368e7a610e42397e960946.hex -v
