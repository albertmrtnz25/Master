
import numpy as np
import math
import matplotlib.pyplot as plt



infile    ="freqdbh.dat" # Fichero de datos. Contiene outputs de GalacTICS
velscale  = 220                # vel Milky Way (km/s)
dist      = 4.5                  # Escala del disco de la Milky Way (kpc)



data= np.genfromtxt(infile, comments='#')[:,0:]
    
radius = data[:, 0]
omegah  = data[:, 1]
vct   = data[:, 4]
vb    = data[:,5]
    
vctot=vct*velscale
vcb=vb*velscale
vhb=np.sqrt((vcb*vcb)+((omegah*radius*velscale)*(omegah*radius*velscale)))
disk=np.sqrt((vctot*vctot)-(vhb*vhb))
print(vctot)
print(vhb)
vhalo=omegah*radius*velscale
plt.plot(radius*dist,vctot)
plt.xlabel('Galactocentric radius (kpc)')
plt.ylabel('Rotation velocity km/s')
plt.xlim(0, 25)
plt.plot(radius*dist,vcb)
plt.plot(radius*dist,disk)
plt.plot(radius*dist,vhalo)
plt.legend(['Total rotation velocity','Bulge rotation velocity','Disk rotation velocity','Halo rotation velocity',])

plt.show()
