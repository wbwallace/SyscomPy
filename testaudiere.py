import sys
sys.path.append("c:\\users\\bill\\my documents\\syscompy")
import smr_io
import audiere
import numpy as np
filepath = "c:\\users\\bill\\my documents\\syscompy\\2004ParkfieldEquake\\BMR06001.ASC"
x, y, z = smr_io.get_smr_data(filepath)

xy = np.column_stack((x,y))
xz = np.column_stack((x,z))
zy = np.column_stack((z,y))

d = audiere.open_device()
wx = d.open_array(x, 200)
wy = d.open_array(y, 200)
wz = d.open_array(z, 200)

wxy = d.open_array(xy, 200)
wxz = d.open_array(xz, 200)
wzy = d.open_array(zy, 200)

wx.pitchshift = 3
wy.pitchshift = 3
wz.pitchshift = 3
wx.play()
