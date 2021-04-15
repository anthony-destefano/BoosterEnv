import sys
import numpy as np
import matplotlib.pyplot as plt

# python .\convert_differential_to_integral_flux.py .\200km_SPE_flux.txt > 200km_SPE_flux_integral.txt
# python .\convert_differential_to_integral_flux.py .\SPE_flux_worst-case.txt > SPE_flux_worst-case_integral.txt
# python .\convert_differential_to_integral_flux.py .\SPE_flux_45.04km.txt > SPE_flux_45.04km_integral.txt
# python .\convert_differential_to_integral_flux.py .\SPE_flux_47.65km.txt > SPE_flux_47.65km_integral.txt

# python .\convert_differential_to_integral_flux.py .\200km_GCR_flux.txt > 200km_GCR_flux_integral.txt
# python .\convert_differential_to_integral_flux.py .\GCR_flux_worst-case.txt > GCR_flux_worst-case_integral.txt
# python .\convert_differential_to_integral_flux.py .\GCR_flux_45.04km.txt > GCR_flux_45.04km_integral.txt
# python .\convert_differential_to_integral_flux.py .\GCR_flux_47.65km.txt > GCR_flux_47.65km_integral.txt

filename = sys.argv[1]

x,y = np.loadtxt(filename, unpack=True)

N = x.shape[0]

yint = np.zeros(N-1)

for i in range(0, N-1):
	if y[i] > 0. and y[i+1] > 0:
		bi = np.log(y[i+1] / y[i]) / np.log(x[i+1] / x[i])

		yint[i] = y[i] * x[i] / (bi + 1.) * ((x[i+1] / x[i])**(bi + 1.) - 1.)

	if i > 0:
		yint[i] = yint[i] + yint[i-1]

yint = yint[-1] - yint # to make an integral flux > x, not < x

for i in range(0, N-1):
	print(x[i], yint[i])