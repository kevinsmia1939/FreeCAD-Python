import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
mpl.rcParams['figure.dpi'] = 200
mpl.rcParams['xtick.labelsize'] = 6
mpl.rcParams['ytick.labelsize'] = 6
mpl.rcParams['axes.labelsize'] = 6
mpl.rcParams['axes.facecolor'] = 'black'

a = np.array([1,2,3])
b = np.array([1,1,1])

bone = np.array([2,2])
bone_y = np.array([0,1])

# plt.plot(a,b,"-o")
# plt.plot(bone,bone_y,"-o")

unit_x = np.append(a,bone)
unit_y = np.append(b,bone_y)
plt.plot(unit_x,unit_y,"-o")

print(unit_x)
print(unit_y)
plt.gca().set_aspect('equal')