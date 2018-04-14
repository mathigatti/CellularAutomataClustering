import sys
import random
import math
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

N = 100

maxPossibleValue = 1000
vals = range(maxPossibleValue)
distribution = [0] * maxPossibleValue

amarillo = 650
hongo = amarillo/2
distribution[hongo] = 0.001
distribution[amarillo] = 0.999
# populate grid with random on/off - more off than on
grid = np.random.choice(vals, N*N, p=distribution).reshape(N, N)
grid[0] = np.array(range(0,maxPossibleValue,maxPossibleValue/N))

# set up animation
fig, ax = plt.subplots()
mat = ax.matshow(grid)

def esHongo(x):
  return x <= hongo

def infectado(x):
  return (x != 0 and random.randint(1, math.pow(2,8-x)) == 1) or (x == 0 and random.randint(1, 10000) == 1)

def update(data):
  global grid

  newGrid = grid.copy()
  for i in range(N):
    for j in range(N):
      vecinos = [grid[i, (j-1)%N], grid[i, (j+1)%N], 
               grid[(i-1)%N, j], grid[(i+1)%N, j]]

      # apply rules
      numVecinosHongos = len(filter(lambda x: esHongo(x),vecinos))
      if esHongo(grid[i,j]):
        newGrid[i,j] = grid[i,j]-0.1*numVecinosHongos
      else:
        if infectado(numVecinosHongos):
            newGrid[i,j] = hongo
        else:
          newGrid[i,j] = grid[i,j]

  # update data
  mat.set_data(newGrid)
  grid = newGrid
  return [mat]

def main(argv, grid=grid, N=N, mat=mat):
  ani = animation.FuncAnimation(fig, update, interval=50, save_count=50)
  plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])

