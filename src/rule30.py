################################################################################
# conway.py
#
# Author: electronut.in
# 
# Description:
#
# A simple Python/matplotlib implementation of Conway's Game of Life.
################################################################################

import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

N = 500
ON = 255
OFF = 0
vals = [ON, OFF]

rule = {(OFF,OFF,OFF): OFF, (OFF,OFF,ON) : ON, (OFF,ON,OFF):ON, (OFF,ON,ON):ON, (ON,OFF,OFF):OFF, (ON,OFF,ON):ON, (ON,ON,OFF):ON, (ON,ON,ON):OFF}

# populate grid with random on/off - more off than on
grid = np.zeros((N,N))
grid[0,int(N/2)] = ON
i = 0

def update(data):
  global grid
  global i
  # copy grid since we require 8 neighbors for calculation
  # and we go line by line 
  newGrid = grid.copy()
  if i < N:
    for j in range(N):
      # compute 8-neghbor sum 
      # using toroidal boundary conditions - x and y wrap around 
      # so that the simulaton takes place on a toroidal surface.

      if i == 0:
        v = np.random.choice([ON,OFF])
        newGrid[i,j] = grid[i,j]
      else:
        if j > 0 and j < N-1:
          newGrid[i,j] = rule[(grid[i-1,j-1],grid[i-1,j],grid[i-1,j+1])]
        else:
          newGrid[i,j] = ON
    i += 1

  # update data
  mat.set_data(newGrid)
  grid = newGrid
  return [mat]

# set up animation
fig, ax = plt.subplots()
mat = ax.matshow(grid)
ani = animation.FuncAnimation(fig, update, interval=50,
                              save_count=50)
plt.show()