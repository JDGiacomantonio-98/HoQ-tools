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
	if n == 0:
		return 1
	return n*fact(n-1)


def compute_acceptance_proba_dss(n1, c1, n2, c2, p, verbose=False):
	proba = 0

	# compute prob. acceptance right at first stage
	for x in range(c1+1):
		proba += ((fact(n1)/(fact(x)*fact(n1-x)))*(p**x)*((1-p)**(n1-x)))

	# compute prob. acceptance at the second stage considering all possible precedent states of d1
	for x in range(c1+1, c2+1):
		acc = 0
		for y in range(c2-x+1):
			acc += ((fact(n2)/(fact(y)*fact(n2-y)))*(p**y)*((1-p)**(n2-y)))
		proba += ((fact(n1)/(fact(x)*fact(n1-x)))*(p**x)*((1-p)**(n1-x)))*acc
	if verbose:
		acc = 0
		for x in range(c1+1):
			acc += c2 + 2 - x
		print(f"Overall Pa: {proba}\n# of items in the sum: {acc}")
	
	return proba

compute_acceptance_proba_dss(30, 1, 60, 2, 0.03, verbose=True)