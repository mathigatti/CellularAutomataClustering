import random
import sys
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from functools import partial

N = 100
ON = 100
OFF = 0
vals = [ON, OFF]

# populate grid with random on/off - more off than on
grid = np.random.choice(vals, N*N, p=[0.01, 0.99]).reshape(N, N)
gridLivingTime = np.random.choice([0], N*N).reshape(N, N)

# set up animation
fig, ax = plt.subplots()
mat = ax.matshow(grid)


def viejo(n):
  return n > 70

def comidaAbuntante(n):
  return n < 10

def update(data, lifespan):
  global grid
  global gridLivingTime
  # copy grid since we require 8 neighbors for calculation
  # and we go line by line 
  newGrid = grid.copy()
  for i in range(N):
    for j in range(N):
      # compute 8-neghbor sum 
      # using toroidal boundary conditions - x and y wrap around 
      # so that the simulaton takes place on a toroidal surface.
      total = (grid[i, (j-1)%N] + grid[i, (j+1)%N] + 
               grid[(i-1)%N, j] + grid[(i+1)%N, j] + 
               grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + 
               grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/8
      # apply Conway's rules
      if grid[i,j] > 0:
        if not viejo(gridLivingTime[i, j]):
          if comidaAbuntante(total):
            newGrid[i,j] = min(grid[i,j]+1, N)
          else:
            newGrid[i,j] = max(grid[i,j]-2, 0)
          gridLivingTime[i,j] += 1

        else:
          if comidaAbuntante(total):
            if random.random() < 0.5:
              newGrid[i,j] = min(grid[i,j]+0.5, N)
              gridLivingTime[i,j] += 1
            else:
              newGrid[i,j] = OFF
              gridLivingTime[i,j] = 0
          else:
            newGrid[i,j] = OFF
            gridLivingTime[i,j] = 0
      else:
        if comidaAbuntante(total):
          gridLivingTime[i,j] = 0
          newGrid[i,j] = 1


  # update data
  mat.set_data(newGrid)
  grid = newGrid
  return [mat]

def main(argv, grid=grid, gridLivingTime=gridLivingTime, N=N, ON=ON, OFF=OFF, mat=mat):
  try:
    lifespan = argv[0]

    updateP = partial(update, lifespan=lifespan)
    ani = animation.FuncAnimation(fig, updateP, interval=50,
                                  save_count=50)
    plt.show()
  except:
    print "Invalid arguments"
    print "Try something like: python life_span_model.py 10"

if __name__ == "__main__":
    main(sys.argv[1:])

