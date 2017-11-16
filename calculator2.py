#!/usr/bin/env python3

import sys

def dispose_arg():
    arg_list = sys.argv[1:]
    employee_info = dict()
    for arg in arg_list:
        info = arg.split(':')
        employee_info[info[0]] = info[1]
    return employee_info    #?????????

def tax_cal(all_salary):
    all_tax = []
    all_insurance = []
    employee_num = []
    salary_list = []

    for key,value in all_salary.items():
        employee_num.append(key)
        salary_list.append(int(value))

    tax_rate = [0.03,0.1,0.2,0.25,0.3,0.35,0.45]    #??
    quick_cal = [0,105,555,1005,2755,5505,13505]    # ?????
    tax_amount = [0,1500,4500,9000,35000,55000,80000] #??????

    for salary in salary_list:
        try:
            # employee_salary = int(salary)   #??????
            insurance = int(salary) * 0.08 + int(salary) * 0.02 \
            + int(salary) * 0.005 + int(salary) * 0.06  #????
            if int(salary) > 3500:
                taxable_income = int(salary) - insurance - 3500 #????????
            else:
                
            all_insurance.append(insurance)
            for i in range(6,-1,-1):
                if taxable_income > tax_amount[i]:
                    tax = taxable_income * tax_rate[i] - quick_cal[i]
                    all_tax.append(tax)
        except:
            raise ValueError

    return all_tax,all_insurance,salary_list,employee_num   #?????????????????????

def after_tax(all_tax,all_insurance,salary_list):
    all_after_tax =[]
    for i in range(len(sys.argv[1:])):
        after_tax_salary = salary_list[i] - all_insurance[i] - all_tax[i]
        all_after_tax.append(after_tax_salary)
    return all_after_tax

if __name__ == '__main__':
    all_salary = dispose_arg()
    all_tax, all_insurance, salary_list, employee_num = tax_cal(all_salary)
    all_after_tax = after_tax(all_tax,all_insurance,salary_list)
    for i in range(len(sys.argv[1:])):
        print(employee_num[i] + ':' + format(float(all_after_tax[i]),'.2f'))
