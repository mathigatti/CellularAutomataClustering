import random
import sys
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from functools import partial

N = 100
A = 0
B = 50
C = 100
Neutro = 200
vals = [A,B,C, Neutro]

# populate grid with random on/off - more off than on
grid = np.random.choice(vals, N*N, p=[0.1, 0.1, 0.1, 0.7]).reshape(N, N)
gridLivingTime = np.random.choice([0], N*N).reshape(N, N)

# set up animation
fig, ax = plt.subplots()
mat = ax.matshow(grid)


def viejo(n):
  return n > 70

def comidaAbuntante(n):
  return n < 10


# A -> B -> C -> A ...

def update(data):
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
      vecinos = [grid[i, (j-1)%N], grid[i, (j+1)%N], 
               grid[(i-1)%N, j], grid[(i+1)%N, j], 
               grid[(i-1)%N, (j-1)%N], grid[(i-1)%N, (j+1)%N], 
               grid[(i+1)%N, (j-1)%N], grid[(i+1)%N, (j+1)%N]]

      # apply Conway's rules
      if grid[i,j] == A:
        hayC = len(filter(lambda x: x==C,vecinos)) > 2
        if hayC:
          newGrid[i,j] = C
          gridLivingTime[i,j] = 0
        else:
          newGrid[i,j] = A
          gridLivingTime[i,j] += 1
      elif grid[i,j] == B:
        hayA = len(filter(lambda x: x==A,vecinos)) > 2
        if hayA:
          newGrid[i,j] = A
          gridLivingTime[i,j] = 0
        else:
          newGrid[i,j] = B
          gridLivingTime[i,j] += 1
      elif grid[i,j] == C:
        hayB = len(filter(lambda x: x==B,vecinos)) > 2
        if hayB:
          newGrid[i,j] = B
          gridLivingTime[i,j] = 0
        else:
          newGrid[i,j] = C
          gridLivingTime[i,j] += 1
      else:
        hayB = len(filter(lambda x: x==B,vecinos)) > 2
        if hayB:
          newGrid[i,j] = B
          gridLivingTime[i,j] = 0
        else:
          hayA = len(filter(lambda x: x==A,vecinos)) > 2
          if hayA:
            newGrid[i,j] = A
            gridLivingTime[i,j] = 0
          else:
            hayC = len(filter(lambda x: x==C,vecinos)) > 2
            if hayC:
              newGrid[i,j] = C
              gridLivingTime[i,j] = 0


  # update data
  mat.set_data(newGrid)
  grid = newGrid
  return [mat]

def main(argv, grid=grid, gridLivingTime=gridLivingTime, N=N, mat=mat):
  ani = animation.FuncAnimation(fig, update, interval=50, save_count=50)
  plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])

