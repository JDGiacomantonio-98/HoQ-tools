# this module should guide the logistic dept. during the acceptance tests on incoming raw material lots

def open_menu():
	pass

def setup():
	pass

def main():
	c = open_menu()
	while True:
		pass # control the test flow


def fact(n):
	'''
	Computes factorial of a given integer using recursion (RecursionError prevents big integers computations)
	'''

	if n == 0:
		return 1
	return n*fact(n-1)

def compute_binom_coeff(n, x):
	'''
	Computes iteratively the binomial coefficient using a super-dried to minimal-terms formula for it. 
	To walk to this result, consider the number of shared multiplicative items between numerators and denominator
	in the usual binomial coefficient formula.

	A special thanks goes to Marco Sebastiano who triggered this idea while helping me cleverly takling an issue
	with my pocket calculator not being able to compute fatorials of integers bigger than 69!
	
	While this can be easily done in Python (as shown here), unfortunately pocket calculators cannot perform
	iterative multiplications. Not good for the exam. :D 
	'''

	acc = 1
	for i in range((n-x-1)+1):
		acc *= ((n-i)/(n-x-i))
		i +=1
	return acc


def compute_acceptance_proba_dss(n1, c1, n2, c2, p, verbose=False, recursive=False):
	'''
	Computes global probability of acceptance of a supplier' lots in  a Double Acceptance Sampling Plan
	'''

	proba = 0

	# compute prob. acceptance right at first stage
	for x in range(c1+1):
		if recursive:
			proba += ((fact(n1)/(fact(x)*fact(n1-x)))*(p**x)*((1-p)**(n1-x)))
		else:
			proba += (compute_binom_coeff(n1, x)*(p**x)*((1-p)**(n1-x)))

	# compute prob. acceptance at the second stage considering all possible precedent states of d1
	for x in range(c1+1, c2+1):
		acc = 0
		if recursive:
			for y in range(c2-x+1):
				acc += ((fact(n2)/(fact(y)*fact(n2-y)))*(p**y)*((1-p)**(n2-y)))
			proba += ((fact(n1)/(fact(x)*fact(n1-x)))*(p**x)*((1-p)**(n1-x)))*acc
		else:
			for y in range(c2-x+1):
				acc += (compute_binom_coeff(n2, y)*(p**y)*((1-p)**(n2-y)))
			proba += (compute_binom_coeff(n1, x)*(p**x)*((1-p)**(n1-x)))*acc
	if verbose:
		acc = c1 +1
		for x in range(c1+1, c2+1):
			acc += (c2 + 1 - x)
		print(f"Overall Pa: {proba}\n# of items in the sum: {acc}")
	
	return proba


compute_acceptance_proba_dss(50, 1, 100, 3, 0.05, verbose=True)