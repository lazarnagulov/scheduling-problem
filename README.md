# Scheduling Problem Implementation using Genetic Algorithm
## Overview
This repository contains an implementation of a genetic algorithm to solve the Scheduling Problem. The solution is written in Python and can be executed by running the following command:

```bash
python3 ./main.py
```
## Data
All input data required for the algorithm is stored in the ```./data_timetable.txt file. ```

An example of the data file format is provided below:
```txt
rooms: A, B, C, D, E
events(name, duration):
NPiEA - Predavanje, 180
Diskretna matematika - Predavanje, 120
Organizacija podataka - Predavanje, 120
NAiNS - Predavanje, 180
...
```

## Configuration
You can customize the algorithm by adjusting constants in the ./common/constants.py file. The default values are:
```python
POPULATION_SIZE = 600
MUTATION_RATE = 0.2
MUTATION_WIDTH = 6
GENERATIONS = 100
ELITISM_RATE = 0.01
```
Feel free to experiment with these values to observe different behaviors of the genetic algorithm.

## Requirements
Make sure you have Python 3.10.11 installed on your system.