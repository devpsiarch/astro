import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np

# reads the planets accual data
def read_planet_data(path):
  with open(path) as f:
      lines = [line.strip() for line in f]

  data = {}

  for i in range(0,len(lines),2):
      name = lines[i].split()[0]
      values = list(lines[i].split()[1:]+lines[i+1].split())
      data[name] = values
  return data

# read some planets jiggle data wich account for errors
def read_planet_jiggle(path):
  with open(path) as f:
      lines = [line.strip() for line in f]
  jiggle = {}
  for i in range(0,len(lines)):
      name = lines[i].split()[0]
      values = list(lines[i].split()[1:])
      jiggle[name] = values
  return jiggle
print(read_planet_jiggle('jiggle.txt'))

def julian_date(day,month,year):
  return (1461*(year+4800+(month-14)/12))/4 + (367*(month-2-12*(month-14)/12))/12 - (3*((year+4900+(month-14)/12)/100))/4 + day - 32075
def julian_number(D,M,Y):
  # or we could have gotten it by 367*Y - (7*(Y + ((M+9)/12)))/4 + (275*M)/9 + D - 730530
  return julian_date(D,M,Y) - 2451545
def calculate_dT(d):
  return (d)/36525
print(julian_number(19,4,1990))

sin_deg = lambda d: np.sin(np.deg2rad(d))
cos_deg = lambda d: np.cos(np.deg2rad(d))

# helps index the attibutes of the planet data
ATTRIBUTES = 6
# help index the planet jiggle
B = 0
C = 1
S = 2
F = 3
# WE FILL OUT THE DATA AS THIS;  a e  I   L   long.peri.   long.node. AND THERE DERIVATIVE
class Body:
  def __init__(self,color,data,name,jiggle=None):
    self.color = color
    self.data_package = data[name]
    self.jiggle = None
    if jiggle != None:
      self.jiggle = jiggle[name]
    self.name = name
  def calculate(self,d):
    dt = calculate_dT(d)

    self.a = float(self.data_package[0]) + float(self.data_package[0+ATTRIBUTES])*dt
    self.e = float(self.data_package[1]) + float(self.data_package[1+ATTRIBUTES])*dt
    self.I = float(self.data_package[2]) + float(self.data_package[2+ATTRIBUTES])*dt
    self.L = float(self.data_package[3]) + float(self.data_package[3+ATTRIBUTES])*dt
    self.long_peri = float(self.data_package[4]) + float(self.data_package[4+ATTRIBUTES])*dt
    self.long_node = float(self.data_package[5]) + float(self.data_package[5+ATTRIBUTES])*dt

    # calculating some essential parameters
    self.w = self.long_peri - self.long_node

    """
    # here are some needed values ... thanks kelpler !
    b = self.a*np.sqrt(1-self.e**2)   # semi minor axis
    f = self.a*self.e                 # current distance
    p = np.power(self.a,1.5)          # period
    """

    self.M = self.L - self.long_peri

    if(self.jiggle != None):
      self.M += float(self.jiggle[B])*dt**2 + float(self.jiggle[C])*sin_deg(float(self.jiggle[F])) + float(self.jiggle[S])*sin_deg(float(self.jiggle[F]))

    # normamizing angles
    self.M = np.mod(self.M + 180, 360) - 180

    # we solve the kepler equation
    e_star = 180/np.pi*self.e
    self.E = self.M + e_star*sin_deg(self.M)
    delta_M = self.M - (self.E - e_star*sin_deg(self.E))
    delta_E = 100
    while delta_E > 1e-6:
      delta_M = self.M - (self.E - e_star*sin_deg(self.E))
      delta_E = delta_M/(1-self.e*cos_deg(self.E))
      self.E += delta_E



    # assigning the positions and all
    self.x_prime = self.a*(cos_deg(self.E) - self.e)
    self.y_prime = self.a*np.sqrt(1-self.e**2)*sin_deg(self.E)
    self.z_prime = 0
    """\matrix{
    x_{ecl} & = & \ (\cos \omega \cos \Omega - \sin \omega \sin \Omega  \cos I) & x'
      & + \ (- \sin \omega \cos \Omega - \cos \omega \sin \Omega \cos I) & y' \cr
    y_{ecl} & = & \ (\cos \omega \sin \Omega + \sin \omega \cos \Omega  \cos I) & x'
      & + \ (- \sin \omega \sin \Omega + \cos \omega \cos \Omega \cos I) & y' \cr
    z_{ecl} & = & \ ( \sin \omega \sin I) & x' & + \ (\cos \omega \sin I)  & y' \cr
    } """
    self.x_ecl = self.x_prime*(cos_deg(self.w)*cos_deg(self.long_node)-sin_deg(self.w)*sin_deg(self.long_node)*cos_deg(self.I)) + self.y_prime*(-sin_deg(self.w)*cos_deg(self.long_node)-cos_deg(self.w)*sin_deg(self.long_node)*cos_deg(self.I))
    self.y_ecl = self.x_prime*(cos_deg(self.w)*sin_deg(self.long_node)+sin_deg(self.w)*cos_deg(self.long_node)*cos_deg(self.I)) + self.y_prime*(-sin_deg(self.w)*sin_deg(self.long_node)+cos_deg(self.w)*cos_deg(self.long_node)*cos_deg(self.I))
    self.z_ecl = self.x_prime*(sin_deg(self.w)*sin_deg(self.I)) + self.y_prime*(cos_deg(self.w)*sin_deg(self.I))

    eps = 23.43928

    self.x_eq = self.x_ecl
    self.y_eq = self.y_ecl*cos_deg(eps) - sin_deg(eps)*self.z_ecl
    self.z_eq = self.z_ecl*cos_deg(eps) + self.y_ecl*sin_deg(eps)

  # prints the data each with there name
  def print(self):
    print(f"a = {self.a}")
    print(f"e = {self.e}")
    print(f"M = {self.M}")
    print(f"w = {self.w}")
    print(f"E = {self.E}")
    print(f"x' = {self.x_prime}")
    print(f"y' = {self.y_prime}")

  # the show function
  def scatter(self,ploter):
    ploter.scatter(self.x_eq,self.y_eq,self.z_eq,color=self.color)

planet_data = read_planet_data('data.txt')
jiggle_data = read_planet_jiggle('jiggle.txt')
print(planet_data)

d = julian_number(1,12,1990)
earth = Body(data=planet_data,name='EM',color='blue')
mars = Body(data=planet_data,name='Mars',color='brown')
venus = Body(data=planet_data,name='Venus',color='orange')
mercury = Body(data=planet_data,name='Mercury',color='grey')
jupiter = Body(data=planet_data,name='Jupiter',color='red',jiggle=jiggle_data)
saturn = Body(data=planet_data,name='Saturn',color='yellow',jiggle=jiggle_data)
uranus = Body(data=planet_data,name='Uranus',color='cyan',jiggle=jiggle_data)
neptune = Body(data=planet_data,name='Neptune',color='purple',jiggle=jiggle_data)


# --- 1. create once ---
fig = plt.figure()
ax  = fig.add_subplot(111, projection='3d')

# 2) Set a “radius” for your view, and equal aspect
R = 1
ax.set_box_aspect((1,1,1))
ax.set_xlim(-R, R)
ax.set_ylim(-R, R)
ax.set_zlim(-R, R)

d = julian_number(20, 12, 1990)
for i in range(100):
    # 3) clear contents, not the axes themselves
    fig = plt.figure()
    ax  = fig.add_subplot(111, projection='3d')

    # recalculate & redraw
    earth.calculate(d)
    mars.calculate(d)
    venus.calculate(d)
    mercury.calculate(d)
    jupiter.calculate(d)
    saturn.calculate(d)
    uranus.calculate(d)
    neptune.calculate(d)

    ax.scatter(0, 0, 0, color="yellow", s=100)  # sun
    earth.scatter(ploter=ax)
    mars.scatter(ploter=ax)
    venus.scatter(ploter=ax)
    mercury.scatter(ploter=ax)
    jupiter.scatter(ploter=ax)
    saturn.scatter(ploter=ax)
    uranus.scatter(ploter=ax)
    neptune.scatter(ploter=ax)

    # 4) re‑apply same aspect & limits (cla() resets them)
    ax.set_box_aspect((1,1,1))
    ax.set_xlim(-R, R)
    ax.set_ylim(-R, R)
    ax.set_zlim(-R, R)

    # 5) draw and pause
    plt.draw()
    plt.savefig(f"plots/fig-{i}.png")
    plt.pause(0.01)

    d += 10

# import shutil
# shutil.make_archive('Planets', 'zip', 'plots')
# from google.colab import files
# files.download('Planets.zip')
#
# files.download('planet.py')
