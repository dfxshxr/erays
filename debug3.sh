#!/bin/bash

python disassembler.py temp/0xf97e0a5b616dffc913e72455fde9ea8bbe946a2b.hex -d > 3.0.disassembler.txt
python graphbuilder.py temp/0xf97e0a5b616dffc913e72455fde9ea8bbe946a2b.hex -d > 3.1.graphbuilder.txt
python lifter.py temp/0xf97e0a5b616dffc913e72455fde9ea8bbe946a2b.hex -d > 3.2.lifter.txt
python optimizer.py temp/0xf97e0a5b616dffc913e72455fde9ea8bbe946a2b.hex -d > 3.3.optimizer.txt
python aggregator.py temp/0xf97e0a5b616dffc913e72455fde9ea8bbe946a2b.hex -d > 3.4.aggregator.txt
python structurer.py temp/0xf97e0a5b616dffc913e72455fde9ea8bbe946a2b.hex -d > 3.5.structurer.txt

python graphbuilder.py temp/0xf97e0a5b616dffc913e72455fde9ea8bbe946a2b.hex -v
python lifter.py temp/0xf97e0a5b616dffc913e72455fde9ea8bbe946a2b.hex -v
