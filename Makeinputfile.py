import numpy as np

meshfile = "glasgow4m.dat"
elevfile = "glasgow_elevation.txt"

nodextemp = []
nodeytemp = []
nodeztemp = []

cellNode1 = []
cellNode2 = []
cellNode3 = []

with open(meshfile) as file:
    for line in file:
        if line.isspace():
            a = line.split()
        else:
            a = line.split()
            b = a[0]
            if a[0] == "node":
                nodextemp.append(float(a[2]))
                nodeytemp.append(float(a[3]))
            elif a[0] == "element":
                cellNode1.append(int(a[3]))
                cellNode2.append(int(a[4]))            
                cellNode3.append(int(a[5]))

with open(elevfile) as file:
      file.readline()
      for line in file:
            a = line.split()
            if a != '':
                nodeztemp.append(float(a[3]))

#转为numpy
nx = np.array(nodextemp)
ny = np.array(nodeytemp)
nz = np.array(nodeztemp)

maxx = nx.max()
minx = nx.min()
maxy = ny.max()
miny = ny.min()

print("xmax:{}, ymax:{}, xmin:{}, ymin:{}\n".format(maxx,maxy,minx,miny))

cellNodes = np.array((len(cellNode1),4))

#for i in range(0,len(cellNode1)):
#    cellNodes[i,0] = cellNode1[i]
#    cellNodes[i,1] = cellNode2[i]  
#    cellNodes[i,2] = cellNode3[i]

#写入inp文件
print("outputing initial condition file\n")
op = open("glasgow.inp", "w")
op.write("\n")
op.write("\n")
op.write("\n")
op.write("{} \n".format(nx.size))
op.write("\n")
op.write("{} \n".format(len(cellNode1)))
op.write("\n")

sldwbd = 0
freebd = 0
for i in range(0, nx.size):

    if (abs(nx[i] - maxx) < 0.1 ) or (abs(ny[i] - maxy) < 0.1 ) or (abs(ny[i] - miny) < 0.1 ):
        nodcod = 5
        sldwbd = sldwbd + 1
    elif (abs(nx[i] - minx) < 0.1 ):
        nodcod = 4
        freebd = freebd + 1
    else:
        nodcod = 0

    op.write("{} {} {} {} {} {} {} {} \n".format(nx[i],ny[i],nz[i],0.0,0.0, 0, (-1 * nz[i]), 0.013))

for i in range(0, len(cellNode1)):
    op.write("{} {} {} {} \n".format(cellNode1[i], cellNode2[i], cellNode3[i], cellNode3[i]))
op.close()

#写入tecplot文件
print("outputing tecplot file\n")
tec = open("glasgowInitialCondition.dat", "w")
tec.write("Initial condition \n")
tec.write("VARIABLES = X, Y, SurfaceElev, u, v, depth, nodcod, roughness\n")
tec.write("ZONE T = \"0 Seconds\", N= {}, E= {}, F=FEPOINT, ET=QUADRILATERAL \n".format(nx.size, len(cellNode1)))

for i in range(0,nx.size):

    if (abs(nx[i] - maxx) < 0.1 ) or (abs(ny[i] - maxy) < 0.1 ) or (abs(ny[i] - miny) < 0.1 ):
        nodcod = 5
    elif (abs(nx[i] - minx) < 0.1 ):
        nodcod = 4
    else:
        nodcod = 0

    tec.write("{}  {}  {}  {}  {}  {}  {}  {} \n".format(nx[i],ny[i],nz[i],0.0,0.0, nodcod, (-1 * nz[i]), 0.013))

for i in range(0, len(cellNode1)):
    tec.write("{}  {}  {}  {} \n".format(cellNode1[i], cellNode2[i], cellNode3[i], cellNode3[i]))
print("this mesh file have {} nodes and {} cells in total \n".format(nx.size, len(cellNode1)))
print("solid wall boundary num:{},Free boundary num:{}\n".format(sldwbd,freebd))
tec.close()

#





