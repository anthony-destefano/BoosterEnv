import sys
import numpy as np
from numpy import vectorize # https://stackoverflow.com/questions/8036878/function-of-numpy-array-with-if-statement
import matplotlib.pyplot as plt

# python .\plot_CREME96.py 4 FLUX SPE_FLUX_COMPARISON .\200km_SPE_flux.txt .\SPE_flux_worst-case.txt .\SPE_flux_45.04km.txt .\SPE_flux_47.65km.txt
# python .\plot_CREME96.py 4 FLUX GCR_FLUX_COMPARISON .\200km_GCR_flux.txt .\GCR_flux_worst-case.txt .\GCR_flux_45.04km.txt .\GCR_flux_47.65km.txt
# python .\plot_CREME96.py 8 FLUX FLUX_COMPARISON .\200km_SPE_flux.txt .\SPE_flux_worst-case.txt .\SPE_flux_45.04km.txt .\SPE_flux_47.65km.txt .\200km_GCR_flux.txt .\GCR_flux_worst-case.txt .\GCR_flux_45.04km.txt .\GCR_flux_47.65km.txt

# python .\plot_CREME96.py 4 LET SPE_LET_COMPARISON .\200km_SPE_LET.txt .\SPE_LET_worst-case.txt .\SPE_LET_45.04km.txt .\SPE_LET_47.65km.txt
# python .\plot_CREME96.py 4 LET GCR_LET_COMPARISON .\200km_GCR_LET.txt .\GCR_LET_worst-case.txt .\GCR_LET_45.04km.txt .\GCR_LET_47.65km.txt
# python .\plot_CREME96.py 8 LET LET_COMPARISON .\200km_SPE_LET.txt .\SPE_LET_worst-case.txt .\SPE_LET_45.04km.txt .\SPE_LET_47.65km.txt .\200km_GCR_LET.txt .\GCR_LET_worst-case.txt .\GCR_LET_45.04km.txt .\GCR_LET_47.65km.txt

# python .\plot_CREME96.py 4 FLUX_INT SPE_FLUX_INT_COMPARISON .\200km_SPE_flux_integral.txt .\SPE_flux_worst-case_integral.txt .\SPE_flux_45.04km_integral.txt .\SPE_flux_47.65km_integral.txt
# python .\plot_CREME96.py 4 FLUX_INT GCR_FLUX_INT_COMPARISON .\200km_GCR_flux_integral.txt .\GCR_flux_worst-case_integral.txt .\GCR_flux_45.04km_integral.txt .\GCR_flux_47.65km_integral.txt
# python .\plot_CREME96.py 8 FLUX_INT FLUX_INT_COMPARISON .\200km_SPE_flux_integral.txt .\SPE_flux_worst-case_integral.txt .\SPE_flux_45.04km_integral.txt .\SPE_flux_47.65km_integral.txt .\200km_GCR_flux_integral.txt .\GCR_flux_worst-case_integral.txt .\GCR_flux_45.04km_integral.txt .\GCR_flux_47.65km_integral.txt

Nfiles = int(sys.argv[1])
plotType = sys.argv[2] # options are [FLUX, FLUX_INT, LET]
plotTitle = sys.argv[3]

xLabel = ''
yLabel = ''

xmin = 0.0
xmax = 1.0

# convert from CREAM96 units to DSNE units
if plotType == 'FLUX':
	xLabel = 'Energy (MeV)'
	yLabel = 'Differential Flux (p+/cm2-s-MeV)'
	xmin   = 1.E3
	xmax   = 1.E5

if plotType == 'FLUX_INT':
	xLabel = 'Energy (MeV)'
	yLabel = 'Integral Flux (p+/cm2-s)'
	xmin   = 1.E3
	xmax   = 1.E5

if plotType == 'LET':
	xLabel = 'LET (MeV-cm2/mg)'
	yLabel = 'Integral Flux (#/cm2-s)'
	xmin   = 1.E0
	xmax   = 1.E2


for i in range(0, Nfiles):

	filename = sys.argv[4 + i]

	x,y = np.loadtxt(filename, unpack=True)

	data_masked = np.ma.masked_where(y == 0.0, y)

	#print(data_masked)

	#print(np.shape(E), np.shape(data))

	plt.loglog(x, data_masked, label=filename)
	plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
# # plt.xscale('symlog')
# # plt.yscale('symlog')

plt.title(plotTitle)
plt.xlabel(xLabel)
plt.ylabel(yLabel)
plt.xlim(xmin, xmax)
plt.legend()
plt.savefig(plotTitle + ".png", dpi=800)
plt.show()