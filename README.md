## Conway's Game of Life

This is a Python implementation of Conway's [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) using Pygame.

---

## Running

Open View.py to execute the program. Using the UI buttons, the simulation can be started, restarted, accelerated, decelerated, or iterated through.
Pre-set configurations can be found in the **assets** folder and can be loaded while the program is running by clicking on the disk button.
At the moment, however, the configuration file to be loaded is hardcoded and must therefore be changed manually by adapting the code on
line 144 in View.py if another configuration file should be loaded. 

---

## Creating Custom Configurations

A configuration file is a simple text file consisting of asteriks (*) and dots (.), where an asterik denotes that the corresponding cell will
be occupied and a dot denotes that the cell will be empty. The number of overall characters (i.e. '.' and '*') need not correspond 
to the number of cells in the grid. However, to ensure an accurate representation of the configuration on the grid, the characters need to be
placed correctly relative to each other as they are intended to be seen on the grid.
For examples on how a configuration file is structured, take a look in the **assets** folder. 
 
