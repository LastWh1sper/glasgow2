from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import numpy as np


filename = "XYCS(2m).TXT"

tempx = []
tempy = []
tempz = []

with open(filename) as file:
    for line in file:
        a = line.split()
        b = a[0][0:2]
        if b != "CS":
            tempx.append(float(a[1]))
            tempy.append(float(a[2]))
            tempz.append(float(a[4]))

x = np.array(tempx)
y = np.array(tempy)
z = np.array(tempz)

xx = np.unique(x)
yy = np.unique(y)

xsize = xx.size
ysize = yy.size

print("the x y size of the dem",xsize,ysize)

Z = z.reshape((ysize,xsize),order = 'F')

print()
X,Y = np.meshgrid(xx,yy)

fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

ls = LightSource(270, 45)
# To use a custom hillshading mode, override the built-in shading and pass
# in the rgb colors of the shaded surface calculated from "shade".
rgb = ls.shade(Z, cmap=cm.gist_earth, vert_exag=0.1)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=rgb,linewidth=0, antialiased=False, shade=False)

ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
#fig.savefig("surface3d_frontpage.png", dpi=2000)  # results in 160x120 px image

ff = open("outcome.txt", "w")
ff.write("x, y, zb\n")
for i in range(0, x.size):
    ff.write('{}   {}   {}\n'.format(x[i], y[i], z[i]))
ff.close()