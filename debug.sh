#!/bin/bash

python graphbuilder.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -d >> 1.graphbuilder.txt
python lifter.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -d >> 2.lifter.txt
python optimizer.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -d >> 3.optimizer.txt
python aggregator.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -d >> 4.aggregator.txt
python structurer.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -d >> 5.structurer.txt
