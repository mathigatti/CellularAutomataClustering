
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import random


N = 100
ON = 255
OFF = 0
vals = [OFF,ON]

# populate grid with random on/off - more off than on
grid = np.random.choice(vals, N*N, p=[0.995,0.005]).reshape(N, N)

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


      umbral = 40

      total = (grid[i, (j-1)%N] + grid[i, (j+1)%N] + 
               grid[(i-1)%N, j] + grid[(i+1)%N, j] + 
               grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + 
               grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/8

      maximo = max(grid[i, (j-1)%N], grid[i, (j+1)%N], 
               grid[(i-1)%N, j], grid[(i+1)%N, j], 
               grid[(i-1)%N, (j-1)%N], grid[(i-1)%N, (j+1)%N], 
               grid[(i+1)%N, (j-1)%N], grid[(i+1)%N, (j+1)%N])


      if total > umbral and grid[i,j] < umbral:
        newGrid[i, j] = maximo
      elif total > umbral and grid[i,j] > umbral:
        newGrid[i, j] = grid[i,j]/1.1

  mat.set_data(newGrid)
  grid = newGrid
  return [mat]

# set up animation
fig, ax = plt.subplots()
mat = ax.matshow(grid)
ani = animation.FuncAnimation(fig, update, interval=50,
                              save_count=50)
plt.show()