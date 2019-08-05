import numpy as np
import cv2

ON = 255
OFF = 0
N = 250

def rule(neighbours,rules):
    if neighbours in rules:
      return ON
    else:
      return OFF

def update(grid,rules):
  newGrid = grid.copy()
  for i in range(1,N-1):
    for j in range(1,N-1):
      newGrid[i,j] = rule((grid[i-1,j],grid[i,j+1],grid[i+1,j],grid[i,j-1]),rules)

  return newGrid

def toTupla(n):
  neighbours = []
  n = "{0:b}".format(n).zfill(4)
  for c in n:
    if c == "0":
      neighbours.append(OFF)
    else:
      neighbours.append(ON)
  return tuple(neighbours)

def toNumber(tupla):
  n = ''
  for t in tupla:
    if t == ON:
      n += "1"
    else:
      n += "0"
  return int(n,2)

def generate(n):
  tuplas = []
  i = 0
  for c in n[::-1]:
    if c == "1":
      tuplas.append(toTupla(i))
    i+=1

  return tuplas

def numberToAutomata(number, steps):
  grid = np.random.choice([ON, OFF], N*N, p=[0.5, 0.5]).reshape(N, N)

  index = "{0:b}".format(number).zfill(256)
  rules = generate(index)

  for step_index in range(steps):
    grid = update(grid,rules)
  cv2.imwrite('images/'+str(number)+'.tiff', grid)
  cv2.imwrite('images/'+str(number)+'.gif', grid)
