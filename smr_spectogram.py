"""make a spectogram of a syscom recorder data file
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import detrend, detrend_linear, detrend_mean, normpdf
from matplotlib.backends.backend_pdf import PdfPages
from scipy.interpolate import UnivariateSpline as scipyUnivariateSpline
import smr_io as sio

# sample files for playing
selftest = "C:\Users\Bill\Documents\SyscomPy\Selftest_sample_ESTA21.ASC"
earthquake = "C:\\Users\\Bill\\Documents\\SyscomPy\\2004ParkfieldQuake_sample_ESTA01.ASC"
funny1 = "C:\Users\Bill\Documents\SyscomPy\FunnyEsta20_11.ASC"
funny2 = "C:\Users\Bill\Documents\SyscomPy\FunnyEsta20_12.ASC"
funny3 = "C:\Users\Bill\Documents\SyscomPy\FunnyEsta20_13.ASC"
funny4 = "C:\Users\Bill\Documents\SyscomPy\FunnyEsta20_14.ASC"
funny5 = "C:\Users\Bill\Documents\SyscomPy\FunnyEsta20_15.ASC"
funny6 = "C:\Users\Bill\Documents\SyscomPy\FunnyEsta20_16.ASC"

filepath = selftest
xdata, ydata, zdata = sio.get_smr_data(filepath)
event_header = sio.get_smr_header(filepath)

esta = event_header["comment"][:7]
testdate = (event_header["int_date"][3:5] + "-" +
            event_header["int_date"][:2] + "-" +
            event_header["int_date"][-2:]) 
psdlabel = esta + " " + testdate

NFFT = 1024
Fs = 200


# use slices to get the portion of the data you want
##data = xdata[:1025]
data = xdata
# exclude the pulse from the histogram for selftests
if event_header["test_sensor"] == "YES":
    hist_data = xdata[:1999]
else:
    hist_data = xdata

# plots
# sublot args are (row column subplot)
# all integers - fills rows first
# subplot and other ploting functions
# return an axis
##ax1 = plt.subplot(221)
ax1 = plt.subplot(141)
plt.plot(data)
ax1.set_xticks(range(0, len(data), 512))

##plt.subplot(222)
ax12 = plt.subplot(142)
Pxx, freqs, bins, im = (plt.specgram(data, 256, Fs))
ax12.axhspan(27, 33, alpha = 0.5, color = "r", fill = False)
ax12.axhspan(57, 63, alpha = 0.5, color = "r", fill = False)

##ax3 = plt.subplot(223)
ax3 = plt.subplot(143)
psdPxx, psdFreqs = plt.psd(data, NFFT, Fs, detrend = detrend_linear)
ax3.set_xscale('log')
#ax3.set_yscale('log')
ax3.text(0.1, 0.05, psdlabel, transform = ax3.transAxes)

##plt.subplot(224)
plt.subplot(144)
plt.hist(hist_data)

plt.figure()
psdPxx, psdFreqs = plt.psd(data, NFFT, Fs, detrend = detrend_linear)
ax21 = plt.gca()
ax21.set_xscale('log')
ax21.text(0.1, 0.05, psdlabel, transform = ax21.transAxes)

# vertical lines at ccritical points
##ax21.axvline(x = 30, alpha = 0.5, color = "r")
##ax21.axvline(x = 50, alpha = 0.5, color = "r")
##ax21.axvline(x = 60, alpha = 0.5, color = "r")
# vertical bars at critical points
ax21.axvspan(28, 32, alpha = 0.2, color = "r")
ax21.axvspan(48, 52, alpha = 0.2, color = "r")
ax21.axvspan(58, 62, alpha = 0.2, color = "r")

plt.figure()
ax31 = plt.subplot(211)
psdPxx, psdFreqs = plt.psd(data, NFFT, Fs, detrend = detrend_linear)
ax31.set_xscale('log')
##ax31.axvline(x = 30, alpha = 0.5, color = "r")
##ax31.axvline(x = 50, alpha = 0.5, color = "r")
##ax31.axvline(x = 60, alpha = 0.5, color = "r")
# vertical bars at critical points
ax31.axvspan(28, 32, alpha = 0.2, color = "r")
ax31.axvspan(48, 52, alpha = 0.2, color = "r")
ax31.axvspan(58, 62, alpha = 0.2, color = "r")
ax31.text(0.1, 0.05, psdlabel, transform = ax31.transAxes)

ax32 = plt.subplot(212)
Pxx, freqs, bins, im = (plt.specgram(data, 256, Fs))
ax32.set_ylabel("frequency")
ax32.set_xlabel("timeslice")
ax32.axhspan(27, 33, alpha = 0.5, color = "r", fill = False)
ax32.axhspan(57, 63, alpha = 0.5, color = "r", fill = False)

plt.figure()
ax41 = plt.subplot(121)
psdPxx, psdFreqs = plt.psd(data, NFFT, Fs, detrend = detrend_linear)
ax41.set_xscale('log')
##ax41.axvline(x = 30, alpha = 0.5, color = "r")
##ax41.axvline(x = 50, alpha = 0.5, color = "r")
##ax41.axvline(x = 60, alpha = 0.5, color = "r")
# vertical bars at critical points
ax41.axvspan(28, 32, alpha = 0.2, color = "r")
ax41.axvspan(48, 52, alpha = 0.2, color = "r")
ax41.axvspan(58, 62, alpha = 0.2, color = "r")
ax41.text(0.1, 0.05, psdlabel, transform = ax41.transAxes)

ax42 = plt.subplot(122)
Pxx, freqs, bins, im = (plt.specgram(data, 256, Fs))
ax42.set_ylabel(ylabel = "frequency", labelpad = 0,
                horizontalalignment = "right")
ax42.set_xlabel("timeslice")
ax42.tick_params(axis = "y", labelleft = "off", labelright = "on")
ax42.axhspan(27, 33, alpha = 0.5, color = "r", fill = False)
ax42.axhspan(57, 63, alpha = 0.5, color = "r", fill = False)

plt.figure()
ax51 = plt.subplot(121)
plt.plot(data)
#ax1.set_xticks([float(x) for x in range(0, len(data), 512)])
ax52 = plt.subplot(122)
n, histbins, patches = plt.hist(hist_data)
##y = scipyUnivariateSpline(histbins, n)
##bincenters = 0.5 * (histbins[1:] + histbins[:-1])
##l = ax52.plot(histbins, y, "r-", linewidth = 2)

pp = PdfPages("foo.pdf")
pp.savefig(1)
pp.savefig(2)
pp.savefig(3)
pp.savefig(4)
pp.savefig(5)
pp.close()
plt.show()

