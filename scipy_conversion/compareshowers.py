import uproot
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

myshowerfile = uproot.open("/home/utente/Lavoro/DE19_R3/b000001/recoshower_250DR_26_11/shower1.root")
mlshowerfile = uproot.open("/home/utente/Lavoro/DE19_R3/b000001/maria_26_01_21/shower1ml.root")

myshower = myshowerfile["treebranch"]
mlshower = mlshowerfile["treebranch"]

#getting arrays

myids = myshower.array("idb")
myplates = myshower.array("plateb")

yb = myshower.array("yb")
zb = myshower.array("zb")
tyb = myshower.array("tyb")

myids = myids[146]
myplates = myplates[146]
yb = yb[146]
zb = zb[146]
tyb = tyb[146]

mlids = mlshower.array("idb")
mlplates = mlshower.array("plateb")
mlyb = mlshower.array("yb")
mlzb = mlshower.array("zb")
mltyb = mlshower.array("tyb")

mlyb = mlyb[0]
mlzb = mlzb[0]
mltyb = mltyb[0]


mlids = mlids[0]
mlplates = mlplates[0]
#check if is there, start comparisons
mlfound = []
mlnotfound = []
for (myid, myplate) in zip(myids,myplates):
    if (myid,myplate) in zip(mlids,mlplates):
        mlfound.append(True)
        mlnotfound.append(False)
    else:
        mlfound.append(False)
        mlnotfound.append(True)

standardfound = []
standardnotfound = []

for (mlid, mlplate) in zip(mlids,mlplates):
    if (mlid,mlplate) in zip(myids,myplates):
        standardfound.append(True)
        standardnotfound.append(False)
    else:
        standardfound.append(False)
        standardnotfound.append(True)

standardonlyyb = yb[mlnotfound]
standardonlyzb = zb[mlnotfound]
standardonlytyb = tyb[mlnotfound]

commonyb = yb[mlfound]
commonzb = zb[mlfound]
commontyb = tyb[mlfound]

mlonlyyb = mlyb[standardnotfound]
mlonlyzb = mlzb[standardnotfound]
mlonlytyb = mltyb[standardnotfound]


dz=315
 
Y_mine = commonyb - commontyb*dz/2
Y_maxe = commonyb + commontyb*dz/2
Z_mine = commonzb - dz/2
Z_maxe = commonzb + dz/2

newlineyz_ecommon = []
for i in range(len(Z_mine)):
 newlineyz_ecommon.append([(Z_mine[i],Y_mine[i]), (Z_maxe[i],Y_maxe[i])])
 lcyz_common = LineCollection(newlineyz_ecommon, colors="yellow", lw=2, label = "common segments,number = {}".format(len(commonyb)))

Y_mine = standardonlyyb - standardonlytyb*dz/2
Y_maxe = standardonlyyb + standardonlytyb*dz/2
Z_mine = standardonlyzb - dz/2
Z_maxe = standardonlyzb + dz/2

newlineyz_estandardonly = []
for i in range(len(Z_mine)):
 newlineyz_estandardonly.append([(Z_mine[i],Y_mine[i]), (Z_maxe[i],Y_maxe[i])])
 lcyz_standardonly = LineCollection(newlineyz_estandardonly, colors="green", lw=2, label = "Standard only segments, number {}".format(len(standardonlyyb)))

Y_mine = mlonlyyb - mlonlytyb*dz/2
Y_maxe = mlonlyyb + mlonlytyb*dz/2
Z_mine = mlonlyzb - dz/2
Z_maxe = mlonlyzb + dz/2

newlineyz_emlonly = []
for i in range(len(Z_mine)):
 newlineyz_emlonly.append([(Z_mine[i],Y_mine[i]), (Z_maxe[i],Y_maxe[i])])
 lcyz_mlonly = LineCollection(newlineyz_emlonly, colors="brown", lw=2, label = "ML only segments,number={}".format(len(mlonlyyb)))
#
f2 = plt.figure()
ax2 = f2.gca()
ax2.set_xlim(-39000, 800)
ax2.set_ylim(0, 100000)

ax2.add_collection(lcyz_mlonly)


ax2.add_collection(lcyz_common)


ax2.add_collection(lcyz_standardonly)

plt.legend()
plt.show()