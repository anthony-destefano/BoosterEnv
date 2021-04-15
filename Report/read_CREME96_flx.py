import sys
import numpy as np
from numpy import vectorize # https://stackoverflow.com/questions/8036878/function-of-numpy-array-with-if-statement
import matplotlib.pyplot as plt

# python .\read_CREME96_flx.py 1 1 SPE_FLUX .\3_2_13_200km_SPE_worst_week.flx 12 > 200km_SPE_flux.txt
# python .\read_CREME96_flx.py 1 1 GCR_FLUX .\3_2_13_200km_GCR.flx 12 > 200km_GCR_flux.txt
# python .\read_CREME96_flx.py 1 1 SPE_LET .\3_2_13_200km_SPE_worst_week_with_heavies_LET.let 17 > 200km_SPE_LET.txt
# python .\read_CREME96_flx.py 1 1 GCR_LET .\3_2_13_200km_GCR_with_heavies_LET.let 17 > 200km_GCR_LET.txt

# python .\read_CREME96_flx.py 3 0 SPE_FLUX .\Booster_45_04km_SPE_worst_week.flx 12 .\Booster_47_65km_SPE_worst_week.flx 12 .\3_2_13_200km_SPE_worst_week.flx 12
# python .\read_CREME96_flx.py 3 0 GCR_FLUX .\Booster_45_04km_GCR.flx 12 .\Booster_47_65km_GCR.flx 12 .\3_2_13_200km_GCR.flx 12

### 3/18/2021

# python .\read_CREME96_flx.py 1 1 SPE_FLUX .\Booster_50km_worst_case_SPE_worst_week.flx 12 > SPE_flux_worst-case.txt
# python .\read_CREME96_flx.py 1 1 GCR_FLUX .\Booster_50km_worst_case_GCR.flx 12 > GCR_flux_worst-case.txt
# python .\read_CREME96_flx.py 1 1 SPE_LET .\Booster_50km_worst_case_SPE_worst_week_LET.let 17 > SPE_LET_worst-case.txt
# python .\read_CREME96_flx.py 1 1 GCR_LET .\Booster_50km_worst_case_GCR_LET.let 17 > GCR_LET_worst-case.txt

# python .\read_CREME96_flx.py 4 0 SPE_FLUX .\Booster_50km_worst_case_SPE_worst_week.flx 12 .\3_2_13_200km_SPE_worst_week.flx 12 .\Booster_45_04km_SPE_worst_week.flx 12 .\Booster_47_65km_SPE_worst_week.flx 12
# python .\read_CREME96_flx.py 4 0 GCR_FLUX .\Booster_50km_worst_case_GCR.flx 12 .\3_2_13_200km_GCR.flx 12 .\Booster_45_04km_GCR.flx 12 .\Booster_47_65km_GCR.flx 12
# python .\read_CREME96_flx.py 4 0 SPE_LET  .\Booster_50km_worst_case_SPE_worst_week_LET.let 17 .\3_2_13_200km_SPE_worst_week_with_heavies_LET.let 17 Booster_47_65km_SPE_worst_week_LET.let 17 Booster_45_04km_SPE_worst_week_LET.let 17
# python .\read_CREME96_flx.py 4 0 GCR_LET  .\Booster_50km_worst_case_GCR_LET.let 17 .\3_2_13_200km_GCR_with_heavies_LET.let 17 Booster_47_65km_GCR_LET.let 17 Booster_45_04km_GCR_LET.let 17

Nfiles = int(sys.argv[1])
toPrint = int(sys.argv[2])
plotType = sys.argv[3] # options are [SPE_FLUX, GCR_FLUX, SPE_LET, GCR_LET]

xScale = 1.
yScale = 1.

xLabel = ''
yLabel = ''

# convert from CREAM96 units to DSNE units
if plotType == 'SPE_FLUX':
	xScale = 1. # MeV
	yScale = 4.*np.pi/100.**2 * 2. # convert from p+/m2-s-sr-MeV to p+/cm2-s-MeV (2x)
	xLabel = 'Energy (MeV)'
	yLabel = 'Differential Flux (p+/cm2-s-MeV) (2x)'

if plotType == 'GCR_FLUX':
	xScale == 1. # MeV
	yScale = 4.*np.pi/100.**2 # convert from p+/m2-s-sr-MeV to p+/cm2-s-MeV
	xLabel = 'Energy (MeV)'
	yLabel = 'Differential Flux (p+/cm2-s-MeV)'

if plotType == 'SPE_LET':
	xScale = 1.E-3 # MeV-cm2/g to MeV-cm2/mg
	yScale = 4.*np.pi/100.**2 * 2. # convert from #/m2-s-sr to #/cm2-s (x2)
	xLabel = 'LET (MeV-cm2/mg)'
	yLabel = 'Integral Flux (#/cm2-s) (x2)'

if plotType == 'GCR_LET':
	xScale = 1.E-3 # MeV-cm2/g to MeV-cm2/mg
	yScale = 4.*np.pi/100.**2 # convert from #/m2-s-sr to #/cm2-s
	xLabel = 'LET (MeV-cm2/mg)'
	yLabel = 'Integral Flux (#/cm2-s)'


for i in range(0, Nfiles):

	filename = sys.argv[4 + i*2]
	Nheader = int(sys.argv[5 + i*2])

	line = np.loadtxt(filename, skiprows = Nheader-2, max_rows = 1, usecols = (0,1,2))

	Emin = line[0]
	Emax = line[1]
	N_E  = int(line[2])

	E = np.logspace(np.log10(Emin), np.log10(Emax), N_E) * xScale

	#print(Emin, Emax, N_E)

	data = np.loadtxt(filename, skiprows = Nheader, max_rows = int(N_E/6))

	data = data.flatten() * yScale



	data_masked = np.ma.masked_where(data == 0.0, data)

	#print(data_masked)

	#print(np.shape(E), np.shape(data))
	if toPrint == 1:
		for i in range(0,N_E):
			print(E[i], data[i])
	if toPrint == 0:
		plt.loglog(E, data_masked, label=filename)
		plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
# # plt.xscale('symlog')
# # plt.yscale('symlog')
if toPrint == 0:
	plt.xlabel(xLabel)
	plt.ylabel(yLabel)
	plt.legend()
	plt.show()