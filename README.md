# Advent of Code 2024

Python solutions for [Advent of Code 2024](https://adventofcode.com/2024).

## Layout

```
day01/
  day01.py        # solution (part_one, part_two, main)
  day01.txt       # puzzle input (git-ignored)
  __init__.py
...
day15/
  day15_viz.py    # optional HTML visualisation generator
day14/
  christmas_tree.png
```

Each day is a self-contained module. `dayNN.py` reads `dayNN.txt` from its own
directory and prints both answers:

```
Part 1: <answer>
Part 2: <answer>
```

## Requirements

- Python 3.12+ (standard library only; no third-party dependencies)

## Running a day

```sh
# from the repository root
python day01/day01.py

# or as a module (uses the package __init__.py)
python -m day01.day01
```

## Inputs

Puzzle inputs (`day*/*.txt`) are personal to each account and are **not**
committed — place your own copy at `dayNN/dayNN.txt`. They are ignored by
`.gitignore`.

## Visualisations

A couple of days ship an optional animated HTML visualiser (standard library
only). It re-simulates the puzzle and writes a self-contained `.html` file
next to the script, which you can open in any browser:

```sh
python day15/day15_viz.py   # -> day15/day15_viz.html
python day20/day20_viz.py   # -> day20/day20_viz.html
```

## Days

| Day | Puzzle | Day | Puzzle |
| --- | ------ | --- | ------ |
| 01 | Historian Hysteria | 14 | Restroom Redoubt |
| 02 | Red-Nosed Reports | 15 | Warehouse Woes |
| 03 | Mull It Over | 16 | Reindeer Maze |
| 04 | Ceres Search | 17 | Chronospatial Computer |
| 05 | Print Queue | 18 | RAM Run |
| 06 | Guard Gallivant | 19 | Linen Layout |
| 07 | Bridge Repair | 20 | Race Condition |
| 08 | Resonant Collinearity | 21 | Keypad Conundrum |
| 09 | Disk Fragmenter | 22 | Monkey Market |
| 10 | Hoof It | 23 | LAN Party |
| 11 | Plutonian Pebbles | 24 | Crossed Wires |
| 12 | Garden Groups | 25 | Code Chronicle |
| 13 | Claw Contraption | | |
