import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import random


# Constantes
alpha = 30


def sen(grados):
    return math.sin(math.radians(grados))

def cos(grados):
    return math.cos(math.radians(grados))


def toIsometric2D(coords):
  x = coords[0]
  y = coords[1]
  z = coords[2]
  u=(x-z)/math.sqrt(2);
  v=(x+2*y+z)/math.sqrt(6);
  return u,v;

def isometric(coords):
  x = coords[0]
  y = coords[1]
  z = coords[2]
  u = x*cos(alpha) + y*cos(alpha+120) + z*cos(alpha-120)
  v = x*sen(alpha) + y*sen(alpha+120) + z*sen(alpha-120)
  return u,v

def norma1(cord1,cord2):
  res = (abs(cord1[0]-cord2[0])+abs(cord1[1]-cord2[1])+abs(cord1[2]-cord2[2]))
  return res

def norma2(cord1,cord2):
  return ((cord1[0]-cord2[0])*(cord1[0]-cord2[0])+(cord1[1]-cord2[1])*(cord1[1]-cord2[1])+(cord1[2]-cord2[2])*(cord1[2]-cord2[2]))

def normainf(cord1,cord2):
  return max(abs(cord1[0]-cord2[0]),abs(cord1[1]-cord2[1]),abs(cord1[2]-cord2[2]))

def dameRandom():
  return random.random()*20-10

def random3dcord():
  return (dameRandom(),dameRandom(),dameRandom())

def cubo():
  xs = []
  ys = []
  zs = []

  for i in range(1000000):
    coordinates = random3dcord()
    if(abs(norma2(coordinates,(0,0,0))-9) < 0.5):
      x, y, z = coordinates
      xs.append(x)
      ys.append(y)
      zs.append(z)
  return xs, ys, zs


def cuboTo2D():
  xs = []
  ys = []

  for i in range(1000000):
    coordinates = random3dcord()
    if(abs(norma1(coordinates,(0,0,0))-9) < 0.01):
      x, y = toIsometric2D(coordinates)
      xs.append(x)
      ys.append(y)
  return xs, ys


def mover(x,y, alpha, distancia, origen, pasos):
  total = np.linspace(0,distancia,pasos)
  x0 = origen[0]
  y0 = origen[1]
  for i in total:
    x.append(x0 + i*sen(alpha))
    y.append(y0 + i*cos(alpha))
  return x,y

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = 100


def mandelbulb():
  imgx = 50
  imgy = imgx
  imgz = imgy
  n = 8
  # drawing area (xa < xb & ya < yb)
  xa = -1.5
  xb = 1.5
  ya = -1.5
  yb = 1.5
  za = -1.5
  zb = 1.5

  maxIt = 256 # max number of iterations allowed
  pi2 = math.pi * 2.0
  # random rotation angles to convert 2d plane to 3d plane
  xy = random.random() * pi2
  xz = random.random() * pi2
  yz = random.random() * pi2
  sxy = math.sin(xy) ; cxy = math.cos(xy)
  sxz = math.sin(xz) ; cxz = math.cos(xz)
  syz = math.sin(yz) ; cyz = math.cos(yz)

  origx = (xa + xb) / 2.0 ; origy = (ya + yb) / 2.0

  xs = []
  ys = []
  zs = []
  colors = []
  for kz in range(imgz):
    c = kz * (zb - za) / (imgz - 1)  + za
    for ky in range(imgy):
        b = ky * (yb - ya) / (imgy - 1)  + ya
        for kx in range(imgx):
            a = kx * (xb - xa) / (imgx - 1)  + xa
            x = a ; y = b ; z = c
            # 3d rotation around center of the plane
            x = x - origx ; y = y - origy
            x0=x*cxy-y*sxy;y=x*sxy+y*cxy;x=x0 # xy-plane rotation
            x0=x*cxz-z*sxz;z=x*sxz+z*cxz;x=x0 # xz-plane rotation 
            y0=y*cyz-z*syz;z=y*syz+z*cyz;y=y0 # yz-plane rotation
            x = x + origx ; y = y + origy

            cx = x ; cy = y ; cz = z
            for i in range(maxIt):
                r = math.sqrt(x * x + y * y + z * z)
                t = math.atan2(math.hypot(x, y), z)
                p = math.atan2(y, x)
                rn = r ** n
                x = rn * math.sin(t * n) * math.cos(p * n) + cx
                y = rn * math.sin(t * n) * math.sin(p * n) + cy
                z = rn * math.cos(t * n) + cz
                if x * x + y * y + z * z > 4.0: break
            if i > 10:
              xs.append(kx)
              ys.append(ky)
              zs.append(kz)
              colors.append(i)
  return xs,ys,zs, colors

x,y,z,colors = mandelbulb()
ax.scatter(x, y, z, c=colors)
plt.show()

#matplotlib.pyplot.scatter(x,y,z, c=colors)
#matplotlib.pyplot.show()
