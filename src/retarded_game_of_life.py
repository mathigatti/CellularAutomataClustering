import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import random

N = 100
ON = 255
OFF = 0
vals = range(256)

# populate grid with random on/off - more off than on
grid = np.random.choice(vals, N*N).reshape(N, N)

def color(n):
    if 0 <= n < 64:
        return 1
    elif 64 <= n < 128:
        return 2
    elif 128 <= n < 192:
        return 3
    else:
        return 4

def update(data):
  global grid
  # copy grid since we require 8 neighbors for calculation
  # and we go line by line 
  newGrid = grid.copy()
  for i in range(N):
    for j in range(N):
      # compute 8-neghbor sum 
      # using toroidal boundary conditions - x and y wrap around 
      # so that the simulaton takes place on a toroidal surface.
      colors = {1:0,2:0,3:0,4:0}

      colors[color(grid[i, (j-1)%N])] += 1
      colors[color(grid[i, (j+1)%N])] += 1
      colors[color(grid[(i-1)%N, j])] += 1
      colors[color(grid[(i+1)%N, j])] += 1
      colors[color(grid[(i-1)%N, (j-1)%N])] += 1
      colors[color(grid[(i-1)%N, (j+1)%N])] += 1
      colors[color(grid[(i+1)%N, (j-1)%N])] += 1
      colors[color(grid[(i+1)%N, (j+1)%N])] += 1

      popularColor = max(colors, key=colors.get)
      cantidad = max(colors.values())
      if cantidad >= 7:
        newGrid[i, j] = abs(popularColor-4)*64
      elif 4 < cantidad < 7:
        newGrid[i,j] = popularColor*64 - 1
      else:
        newGrid[i, j] = grid[i,j]
  mat.set_data(newGrid)
  grid = newGrid
  return [mat]

# set up animation
fig, ax = plt.subplots()
mat = ax.matshow(grid)
ani = animation.FuncAnimation(fig, update, interval=50,
                              save_count=50)
plt.show()