We can clearly separate the whole process in three stages (capturing, solving, executing). This document focuses on **solving**.

# 1. Directory structure

Solvers will be placed in the `games/` directory. For the game *GAME*, all files will be placed in `games/GAME/`.
All game names *MUST* be in lowercase.

#### In this directory we will have at least the following files:
* `capture.py`, which uses `core/capture` to take a picture, undistort it and extract features it needs.
This file will output some text to stdout as specified in the **formats** section below.
* `execute.py`, which will read *solve*'s output and communicate with the 3D printer to solve the game.
* `setup.py`, which will contain setup information for this specific game.
This setup file will have it's own document explaining it's contents.

#### There are also the following files:
* `solve`: An executable that will read the problem on it's standard input and write the steps to solve it on its standard output.
This file will not be tracked by git.
* `src/`: All sources needed to compile the `solve` executable.
* `Makefile`: A makefile with at least a target named `solve`.

Exceptionally if `solve` can be a standalone script, the `src/` and `Makefile` may be omitted.
In this case the script must still have exactly the name `solve`, and it must be executable from the command line by running
`./solve < input`, where input is the problem as described below.

#### Other files

Other files may be included if it's required, but generally it's preferred to use only the files above.


# 2. `solve` input format

The `solve` script gets utf-8 encoded text on it's stdin.
### non grid based games
The input format is decided by the author of the problem.

### grid based games
Since for now we're always working with grid based problems, the solver's input format will be the following:

A line containing two integers **R** and **C** representing the number of rows and columns of the grid.
**R** lines follow. Each line contains **C** *cell values* (integers) that represent the contents of the cell that it represents.

#### Notes about cell values
* Value -1 is reserved for an empty cell or a background cell.
* Values 0-9 are reserved for the digits 0-9 in games with single digit numbers on the cells.
* Other values may be used freely. It is good practice to define what values mean in constants at the top of the solver.

#### Example input

For the game *Unruly* and the following input image:

<img width="242" alt="screen shot 2017-07-01 at 15 35 29" src="https://user-images.githubusercontent.com/4309591/27762471-017a844a-5e73-11e7-94e6-ce120c4fa3c9.png">

An example output can be:
```
10 10
-1 -1 -1 -1  0 -1 -1 -1  0 -1
-1 -1 -1 -1 -1  1 -1 -1 -1  1
-1  0 -1 -1 -1  1 -1 -1 -1 -1
-1 -1 -1 -1  0 -1 -1 -1  1 -1
-1  0 -1 -1 -1 -1 -1  0 -1  1
-1 -1  1 -1 -1 -1 -1 -1 -1  1
-1 -1 -1  0 -1 -1  1 -1  1 -1
-1 -1  0 -1 -1 -1  1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1  1
 1  0 -1 -1 -1 -1 -1  0 -1  1
```

As per the guidelines above, `-1`is used for background (grey) squares.
Since there are no numbers in this game, `0` is used for black and `1`is used for white.

# 3. `solve` output format

After the solver solves the game, there will be a solved state. 
We don't care about this state, we just want to know how to get to it.
The output of the solver will give us this and only this information.

#### Assumptions
* We know the size of the grid in millimeters, the location of the phone on the printer and the height of the screen.
This way the solver can be abstract and does not need to worry about the low level details and calibrating a 3D printer,
providing a better modularization for the project.
* Coordinate system of the 3D printer is in the range [0,1] for both x and y axis.
This range represents the screen size, the point (0,0) will be on the upper right corner of the screen.
There will be a way in the config file to let the framework know where the grid is located inside the screen,
but the solver does not need to know, as it will have it's own high level API.


The `core/execute` will be used to send the output of the `execute.py`
The output is structured in lines that represent **commands**.
A command is a high level description that tells the 3D printer what to do without needing to get into gcode or communication.
The syntax of a command is the following:
`<command> [param1 [param2...]]`

Available commands are:
* `move R C`: moves the printer to row R and column C of the grid
* `click R C`: single clicks the screen, if R and C are not given it clicks at the current position
* `dclick R C`: same as click, but double clicks
* `lclick R C`: same as click, but long clicks
* `swipe R1 C1 R2 C2`: swipes from R1 C1 to R2 C2
* `delay <ms>`: waits for ms milliseconds
* `movemm x y`: moves x mm in the x direction and y mm in the y direction.
This should only be used for debugging (and remember X and Y are in reverse order of R and C)

Commands are executed as they are printed to stdout.












