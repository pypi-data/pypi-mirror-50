from decimal import getcontext
from decimal import Decimal as d
from math import atan

def pi(precision):
	getcontext().prec = precision
	return d(4) * (d(4) * atan(d(1) / d(5)) - atan(d(1) / d(239)))

def super_square_root(z, a=1., b=4., prec=0.000000000001):
	""" super square root, inverse of y = x^x
		iterative binary search """

	while True:
		c = (a + b) / 2
		cc = c ** c
		if abs(z - cc) < prec:
			return c
		if cc > z:
			b = c
		elif cc < z:
			a = c
		else:
			raise RuntimeError("Should not happen")
		if a == b:
			raise ValueError("Interval invalid")

import numpy as np
assert np.allclose([super_square_root(4.), super_square_root(27.)], [2., 3.])
