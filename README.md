# Rubik's Cube Solver

## 1. Author
Santiago Torrico

## 2. Project Description
This project consists of a Python-based Rubik's Cube solver designed to explore algorithms involved in solving the 3x3 Rubik's Cube through coding. The current version can load a cube's state from a file, perform specific twist operations, and validate cube configurations we also use 3 different heuristics trying to achieve the best way to solve the rubik cube.

## 3. Environment Requirements
- **Programming Language**: Python 3.8 or higher
- No external dependencies are required for the basic functionalities.

## 4. User Manual

### 4.1 Cube State Encoding Format for Loading from a Text File
The Rubik's Cube state should be encoded in a text file as follows:

Each line represents one row of a face, and each face is separated by a newline. The colors are denoted by single letters (e.g., 'w' for white, 'r' for red, etc.). The file should contain a total of 6 faces, each face having 3 lines of 3 characters, representing a standard 3x3 Rubik's Cube.

Example of a file for a solved 3x3 Rubik's Cube: inside file sample_cube.txt 


