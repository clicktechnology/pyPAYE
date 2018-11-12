#!/usr/bin/env python
# coding=utf-8
from taxation import Taxation

# First create an instance of the Taxation class, with the given parameters.

myEmployee = Taxation(full_time=True, student_loan=True, hours_per_week=40, tax_year='2018-2019')

# And let's do a really a simple construction for beginners..

tom_smith_salary = 50000  # Set the annual salary variable.

# Show Tom Smith's PAYE / NI and other payroll taxes.  'True' in this context means Monthly amounts are calculated.

print("Tom Smith's salary is £{:6,.2f} p/a and monthly PAYE is £{:6,.2f}".format(tom_smith_salary,
                                                                                 myEmployee.calculate_paye(
                                                                                     tom_smith_salary, True)))

# Show Tom Smith's PAYE / NI and other payroll taxes.  'False' in this context means Annual amounts are calculated.

print("Tom Smith's salary is £{:6,.2f} p/a and annual PAYE is £{:6,.2f}".format(tom_smith_salary,
                                                                                myEmployee.calculate_paye(
                                                                                    tom_smith_salary, False)))

# Now let's calculate some values using good data and print out a small tax receipt for it in each case.

known_values = (
    #   (salary, Student Loan Repayment Plan - 0 = No student loan repayments, 1 = Plan 1, 2 = Plan 2)
    (6000, 1),
    (23000, 0),
    (43000, 1),
    (52000, 2),
    (102500, 2),
    (105000, 1),
    (130000, 0),
    (163000, 0),
    (289000, 1),
    (344000, 0)
)

for annual_salary, sl_plan in known_values:
    myEmployee.print_tax_ticket(annual_salary, sl_plan)
