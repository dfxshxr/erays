#!/bin/bash

python disassembler.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -d > 1.0.disassembler.txt
python graphbuilder.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -d > 1.1.graphbuilder.txt
python lifter.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -d > 1.2.lifter.txt
python optimizer.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -d > 1.3.optimizer.txt
python aggregator.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -d > 1.4.aggregator.txt
python structurer.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -d > 1.5.structurer.txt

python graphbuilder.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -v
python lifter.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -v
python optimizer.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -v
python aggregator.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex -v
python structurer.py temp/0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea.hex