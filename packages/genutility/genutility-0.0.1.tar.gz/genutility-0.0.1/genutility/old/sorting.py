from __future__ import absolute_import, division, print_function, unicode_literals

def low_sort(l):
	#inplace

	x, z = 0, 0
	while x < len(l) - 1:
		try:
			if l[z] > l[z+1]:
				l[z], l[z+1] = l[z+1], l[z]
			else:
				x += 1
			z += 1
		except IndexError:
			x, z = 0, 0
	return l

def cycle_sort(l):
	n = len(l)
	for cycleStart in range(0, n - 1):
		item = l[cycleStart]
		pos = cycleStart
		for i in range(cycleStart + 1, n):
			if l[i] < item:
				pos += 1
		if pos == cycleStart:
			continue
		while item == l[pos]:
			pos += 1
		l[pos], item = item, l[pos]
		while pos != cycleStart:
			pos = cycleStart
			for i in range(cycleStart + 1, n):
				if l[i] < item:
					pos += 1
			while item == l[pos]:
				pos += 1
			l[pos], item = item, l[pos]
	return l

def cycle_sort_2(l): # does this one work?
	for i in range(len(l)):
		if i != l[i]:
			n = i
			while True:
				tmp = l[n]
				if n != i:
					l[n] = last_value
				last_value = tmp
				n = last_value
				if n == i:
					l[n] = last_value
					break

def divide(l, left, right, pivot):
	#inplace

	i = left
	j = right - 1
	pivot_val = l[pivot]

	while i < j:
		while (l[i] <= pivot_val and i < right):
			i = i + 1
		while (l[i] >= pivot_val and j > left):
			j = j - 1
		if i < j:
			l[i], l[j] = l[j], l[i]

	if l[i] > pivot_val:
		l[i], l[right] = l[right], l[i]
	return i

def _quick_sort(l, left, right):
	ret = []
	if left < right:
		pivot = l[right]
		pivot = divide(l, left, right, pivot)
		_quick_sort(l, left, pivot - 1)
		_quick_sort(l, pivot + 1, right)

def quick_sort(l):
	return _quick_sort(l, 0, len(l)-1)

if __name__ == "__main__":
	from random import shuffle

	l = list(range(20))
	shuffle(l)

	a = l.copy()
	low_sort(a)

	b = cycle_sort(l)

	c = l.copy()
	cycle_sort_2(c)

	d = l.copy()
	quick_sort(d)

	truth = sorted(l)
	assert a == truth
	assert b == truth
	assert c == truth
	assert d == truth
