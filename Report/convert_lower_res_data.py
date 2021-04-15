import sys
import numpy as np
from numpy import vectorize # https://stackoverflow.com/questions/8036878/function-of-numpy-array-with-if-statement
import matplotlib.pyplot as plt


# python .\convert_lower_res_data.py SPE_LET_worst-case.txt 1. 87. 50 > SPE_LET_low-res.txt
# python .\convert_lower_res_data.py GCR_LET_worst-case.txt 1. 87. 50 > GCR_LET_low-res.txt

# python .\convert_lower_res_data.py SPE_flux_worst-case.txt 3900. 1.E5 50 > SPE_flux_low-res.txt
# python .\convert_lower_res_data.py GCR_flux_worst-case.txt 3900. 1.E5 50 > GCR_flux_low-res.txt

# python .\convert_lower_res_data.py SPE_flux_worst-case_integral.txt 3500. 9.5E4 50 > SPE_flux_integral_low-res.txt
# python .\convert_lower_res_data.py GCR_flux_worst-case_integral.txt 3500. 9.5E4 50 > GCR_flux_integral_low-res.txt

def y_power_law(x0, x1, y0, y1, x):
	return y0 * (x/x0)**(np.log(y1/y0) / np.log(x1/x0))


def get_y(x_vec, y_vec, x):
	i = 0

	while i < x_vec.size and x > x_vec[i]:
		i = i + 1

	i = i - 1
	if i < 0 or i > x_vec.size - 2:
		return 0.
	else:
		return y_power_law(x_vec[i], x_vec[i+1], y_vec[i], y_vec[i+1], x)

vget_y = vectorize(get_y)


filename = sys.argv[1]
xmin = float(sys.argv[2])
xmax = float(sys.argv[3])
Nx   = int(sys.argv[4])


x_data, y_data = np.loadtxt(filename, unpack=True)

x_low_res = np.logspace(np.log10(xmin), np.log10(xmax), Nx)

#y_low_res = vget_y(x_data, y_data, x_low_res)

for i in range(0, Nx):
	y_low_res = get_y(x_data, y_data, x_low_res[i])
	print(x_low_res[i], y_low_res)