#!/usr/bin/env python3

import sys

def check_arg():
	if len(sys.argv) > 2:
		raise ValueError()
	try:
		salary = int(sys.argv[1])
	except:
		raise ValueError()
	else:
		return salary

def tax(salary):
#tax_salary为应纳税额，deduct为速算扣除数
	tax_salary = salary - 3500
	if tax_salary < 1500:
		tax_rate = 0.03
		deduct = 0
	elif tax_salary < 4500:
		tax_rate = 0.1
		deduct = 105
	elif tax_salary < 9000:
		tax_rate = 0.2
		deduct = 555
	elif tax_salary < 35000:
		tax_rate = 0.25
		deduct = 1005
	elif tax_salary < 55000:
		tax_rate = 0.3
		deduct = 2755
	elif tax_salary < 80000:
		tax_rate = 0.35
		deduct = 5505
	else:
		tax_rate = 0.45
		deduct = 13505
	return tax_salary,tax_rate,deduct
		
if __name__ == '__main__':
	try:
		salary = check_arg()
		data = tax(salary)
		#print(data)
		tax_count = data[0] * data[1] - data[2]
		print(format(tax_count,".2f"))
	except ValueError:
		print("Parameter Error")
