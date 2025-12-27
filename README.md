# 3D_Minesweeper
Are you feeling bored only playing too much 2D minesweeper? <br>
Are you tired of the game being a flat object?<br>
Are you thinking that you are a master of the game already?

You can think otherwise with this new implementation of a 3D minesweeper!

This is be made fully with python's pygame library



## Features
1. Instead of having 8 sides for every tile, there is now up 26 sides that can possibly have a mine with every open square (or is it a cube)
2. You can rotate the block and zoom into each layers, uncovering more and more mines as you do so!

Note: **Cheat function is not compatible with larger boards because the backtracking algorithm takes too long to run D:**


## Controls
WASDRF keys to move the 3D cube to different orientation
- W to flip forwards
- A to flip leftwards
- S to flip backwards
- D to flip rightwards
- R to turn rightwards
- F to turn leftwards

Arrow keys to switch between the layers of the 3D cube
- Upper arrow key to move upwards
- Lower arrow key to move downwards

Clicking
- Left click to reveal cell(s)
- Right click to flag cell(s)



## How To Access This Game?
1. Download all the files inside the src folder / clone this repository
2. Open up the src folder inside the command prompt
3. Enter 'python3 main.py' in the command prompt



## Requirements
1. Install Python version 3.0 and beyond

If python is not installed, refer to https://www.python.org/downloads/

2. Ensure you have the pygame module

If pygame module is missing, enter 'pip install pygame' inside your command prompt

3. Have a computer!



## Upcoming Improvements
1. When hovering over a clickable button, cursor change to click3
2. Improve cheat run speed
3. Improve UI