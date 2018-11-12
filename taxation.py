#!/usr/bin/env python
# coding=utf-8
"""
    Use the Taxation class to return the payable amounts for the following taxes for a given salary in
    the United Kingdom.

    1. PAYE
    2. Employee National Insurance
    3. Employer's National Insurance
    4. Student Loans repayment for plan 1 and plan 2 repayments.

    PAYE tax data is for 2018-2019 and is taken from the tables at

    https://www.gov.uk/income-tax-rates

    PAYE tax data is for 2016-2017, 2017-2018 and is taken from the tables at

    https://www.gov.uk/income-tax-rates/previous-tax-years

    The algorithm was checked against the following sources for accuracy.

    http://tools.hmrc.gov.uk/hmrctaxcalculator/screen/Personal+Tax+Calculator/en-GB/summary?user=guest
    https://listentotaxman.com

    National Insurance (NI) and Employer's NI tax data is for 2016-2017 and is taken from the tables at

    https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2016-to-2017
    https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2017-to-2018
    https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2018-to-2019

    under the sections "Class 1 National Insurance thresholds" and "Student loan recovery"
"""

__version__ = "0.1.6"


class Taxation:
    def __init__(self, full_time=True, student_loan_plan=None, hours_per_week=40, **kwargs):
        # define class variables.
        self.__version__ = __version__
        self.full_time = full_time
        self.tax_table_all_data = {

            'tax-year': ['2016-2017', '2017-2018', '2018-2019'],

            # Section from link above entitled "Tax thresholds, rates and codes"

            'personal_allowance_reduction_point': [100000.00, 100000.00, 100000.00],
            'default_personal_allowance': [11000.00, 11500.00, 11850.00],

            'basic_rate_threshold': [11000.00, 11500.00, 11850.00],
            'higher_rate_threshold': [43000.00, 45001.00, 46351.00],
            'additional_rate_threshold': [150000.00, 150000.00, 150000.00],

            'basic_tax_rate': [0.20, 0.20, 0.20],
            'higher_tax_rate': [0.40, 0.40, 0.40],
            'additional_tax_rate': [0.45, 0.45, 0.45],

            # Section from link above entitled "Class 1 National Insurance thresholds"

            'lower_earnings_limit': [5824.00, 5876.00, 6032.00],
            'primary_threshold': [8060.00, 8164.00, 8424.00],
            'secondary_threshold': [8112.00, 8164.00, 8424.00],
            'upper_secondary_threshold_U21': [43000.00, 45000.00, 46350.00],
            'apprentice_upper_secondary_threshold_U25': [43000.00, 45000.00, 46350.00],
            'upper_earnings_limit': [43000.00, 45000.00, 46350.00],

            # Section from link above entitled "Class 1 National Insurance rates"

            'lel_to_pt': [0.0, 0.0, 0.0],
            'pt_to_uel': [0.12, 0.12, 0.12],
            'uel_and_above': [0.02, 0.02, 0.02],

            # Section from link above entitled "Employer (secondary) contribution rates"

            'employer_lel_to_pt': [0.0, 0.0, 0.0],
            'employer_pt_to_uel': [0.1380, 0.1380, 0.1380],
            'employer_uel_and_above': [0.1380, 0.1380, 0.1380],

            # Section from link above entitled "Student loan recovery"
            # https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2016-to-2017#student-loan-recovery

            'annual_repayment_threshold_plan_1': [17495.00, 17775.00, 18330.00],  # From tax threshold table, Plan 1.
            'annual_repayment_threshold_plan_2': [21000.00, 21000.00, 25000.00 ],  # From tax threshold table, Plan 2.
            'sl_interest_rate': [0.09, 0.09, 0.09]  # 9% for 2016-2017, 2017-2018, 2018-2019
        }
        self.hours_per_week = hours_per_week
        if not 'tax_year' in kwargs:  # If a value for tax_year is not given, assume it is '2016-2017' for backwards compatibility.
            kwargs = {'tax_year': '2016-2017'}
        self.tax_table = self.set_rates_and_values(**kwargs)

        if not 'student_loan_plan' in (0,1,2):
            self.student_loan_plan = 0
        else:
            self.student_loan_plan = student_loan_plan


    def set_rates_and_values(self, tax_year):

        """ Given the correct tax year value, read the limits, rates and threshold values from the main tax table to a
        matching dictionary, with only thos year's values in it.

        :param tax_year: must be a string of the form '2015-2016', '2016-2017' etc.  This year value must be in the
        tax_table_all_data['tax-year'] dictionary, set in the __init__ section of the class, above.
        :return: Either the dictionary object tax_table or FALSE if the tay_year date was not found.
        """

        tax_table = {}
        try:
            index = self.tax_table_all_data['tax-year'].index(tax_year)  # Find the index of the tax year value.
        except ValueError:
            index = False  # The tax year was not found, so return FALSE from the function.
            return (index)

        for k, dk in self.tax_table_all_data.iteritems():  # Read the elements of the dictionary for the given index into a new dictionary called tax_table.
            tax_table[k] = dk[index]

        return (tax_table)  # Return the tax_table dictionary for use.

    def is_valid_number(self, myinput):
        """Check to see if input is a number.
        :type myinput: the element under analysis.
        """
        try:
            if myinput < 0:
                self.error_message = 'The value given is less than zero'
                return False
            elif isinstance(myinput, basestring):
                self.error_message = 'The value given is a string, not a number or float'
                return False
            else:
                myinput = float(myinput)
                return True
        except ValueError, e:
            self.error_message = 'Error is : {}'.format(e)
            return False

    def get_version(self):
        return self.__version__

    def calculate_employee_ni(self, salary, monthly=True):
        """
        Calculates employee's monthly National Insurance contribution for a given annual salary.
        :param salary : This is the annual salary for which employee NI is to be calculated.
        :param monthly : Returns the monthly amount if set to True, returns the annual amount if set to False.
        """
        try:
            if not self.is_valid_number(salary):
                raise ValueError('Error - The input value >>{}<< is not valid.  '
                                 '{}.  Try again.'.format(salary, self.error_message))

            nic = 0

            if salary > self.tax_table['upper_earnings_limit']:
                taxable_amount = salary - self.tax_table['upper_earnings_limit']
                nic += taxable_amount * self.tax_table['uel_and_above']
                salary -= taxable_amount

            if self.tax_table['primary_threshold'] < salary <= self.tax_table['upper_earnings_limit']:
                taxable_amount = salary - self.tax_table['primary_threshold']
                nic += taxable_amount * self.tax_table['pt_to_uel']
                salary -= taxable_amount

            if 0 <= salary <= self.tax_table['primary_threshold']:
                taxable_amount = salary
                nic += taxable_amount * self.tax_table['lel_to_pt']
                salary -= taxable_amount

            if monthly:
                return round(nic / 12, 2)  # Return MONTHLY nic amount
            else:
                return round(nic, 2)  # Return ANNUAL nic amount

        except ValueError, error_message:
            print error_message
            return False

    def calculate_employer_ni(self, salary, monthly=True):
        """
        Calculates employer's monthly National Insurance contribution for a given annual salary.
        :param salary : This is the annual salary for which employer NI is to be calculated.
        :param monthly : Returns the monthly amount if set to True, returns the annual amount if set to False.
        """

        try:
            if not self.is_valid_number(salary):
                raise ValueError('Error - The input value >>{}<< is not valid.  '
                                 '{}.  Try again.'.format(salary, self.error_message))
            nic = 0

            # Calculate Employer's NICs

            if salary > self.tax_table['upper_earnings_limit']:
                taxable_amount = salary - self.tax_table['upper_earnings_limit']
                nic += taxable_amount * self.tax_table['employer_uel_and_above']
                salary -= taxable_amount

            if self.tax_table['secondary_threshold'] < salary <= self.tax_table['upper_earnings_limit']:
                taxable_amount = salary - self.tax_table['secondary_threshold']
                nic += taxable_amount * self.tax_table['employer_pt_to_uel']
                salary -= taxable_amount

            if 0 <= salary <= self.tax_table['secondary_threshold']:
                taxable_amount = salary
                nic += taxable_amount * self.tax_table['employer_lel_to_pt']
                salary -= taxable_amount

            if monthly:
                return round(nic / 12, 2)  # Return MONTHLY nic amount
            else:
                return round(nic, 2)  # Return ANNUAL nic amount

        except ValueError, error_message:
            print error_message
            return False

    def calculate_paye(self, salary, monthly=True):
        """
        Calculate the employee's monthly PAYE contribution for a given annual salary.
        :param salary : This is the annual salary for which PAYE is to be calculated.
        :param monthly : If set to True, the function returns the monthly PAYE amount payable.  Set to False,
        it returns the annual PAYE payable.
        """

        try:
            if not self.is_valid_number(salary):
                raise ValueError('Error - The input value >>{}<< is not valid.  '
                                 '{}.  Try again.'.format(salary, self.error_message))

            original_salary = salary
            paye = 0
            personal_allowance = self.tax_table['default_personal_allowance']

            basic_rate_threshold = self.tax_table['basic_rate_threshold']
            higher_rate_threshold = self.tax_table['higher_rate_threshold']
            additional_threshold = self.tax_table['additional_rate_threshold']

            # STEP 1 : Check to see if salary is even considered for PAYE.
            if salary <= personal_allowance:
                return 0.00

            # STEP 2 : Calculate personal allowance

            # Your Personal Allowance goes down by £1 for every WHOLE * £2 that your adjusted net income
            # is above £100,000.  This means your allowance is zero if your income is £122,000 or above.
            # https://www.gov.uk/income-tax-rates/income-over-100000
            # http://tools.hmrc.gov.uk/hmrctaxcalculator/screen/Personal+Tax+Calculator/en-GB/summary?user=guest

            if salary > self.tax_table['personal_allowance_reduction_point']:

                personal_allowance_reduction = int((salary - self.tax_table['personal_allowance_reduction_point']) / 2)
                personal_allowance -= personal_allowance_reduction
                if personal_allowance < 0:
                    personal_allowance = 0

            # STEP 3: Check the highest tax bracket and remove it.

            if salary > additional_threshold:
                taxable_chunk = salary - additional_threshold
                paye += taxable_chunk * self.tax_table['additional_tax_rate']
                salary -= taxable_chunk

            # STEP 4: Check the additional to higher rate tax bracket, calculate the tax in this bracket and remove it.

            if higher_rate_threshold < salary <= additional_threshold:
                taxable_chunk = salary - personal_allowance - (higher_rate_threshold - basic_rate_threshold)
                paye += taxable_chunk * self.tax_table['higher_tax_rate']
                salary -= taxable_chunk

            # STEP 5: Check the basic rate to additional rate tax bracket, calculate the tax in this bracket and
            # remove it.

            if basic_rate_threshold < salary <= higher_rate_threshold:

                if original_salary > higher_rate_threshold:
                    taxable_chunk = higher_rate_threshold - basic_rate_threshold
                else:
                    taxable_chunk = salary - personal_allowance

                paye += taxable_chunk * self.tax_table['basic_tax_rate']
                salary -= taxable_chunk

            # STEP 6 : Return the values for PAYE, rounded to 2 DP

            if monthly:
                return round(paye / 12, 2)  # Return MONTHLY amount
            else:
                return round(paye, 2)  # Return ANNUAL amount

        except ValueError, error_message:
            print error_message
            return False

    def calculate_student_loans(self, salary, plan, monthly=True):
        """
        Calculates employee's monthly Student Loan repayments for a given annual salary.

        https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2016-to-2017#student-loan-recovery

        :param salary : This is the annual salary for which Student Loan repayments are to be calculated.
        :param plan : Calculates the repayable amount according to the plan selected.
        :param monthly : If set to True, the function returns the monthly Student Loan repayments payable.
        Set to False, it returns the annual Student Loan repayments payable.
        """

        try:
            if not self.is_valid_number(salary):
                raise ValueError('Error - The input value >>{}<< is not valid.  '
                                 '{}.  Try again.'.format(salary, self.error_message))

            if plan == 0:
                return 0.00
            if plan == 1:
                annual_repayment_threshold = self.tax_table['annual_repayment_threshold_plan_1']
            elif plan == 2:
                annual_repayment_threshold = self.tax_table['annual_repayment_threshold_plan_2']
            else:
                raise ValueError('Error - The repayment plan value can only be 0, 1 or 2. >>{}<< is not valid.'.
                                 format(plan, self.error_message))

            if salary > annual_repayment_threshold:  # Annual salary exceeds threshold.  Let's charge tax.
                salary -= annual_repayment_threshold
                sl_repayment = int(
                    salary * self.tax_table['sl_interest_rate'])  # Round result down to nearest whole number.
            else:
                sl_repayment = 0.00

            if monthly:
                return round(sl_repayment / 12, 2)  # Return MONTHLY amount
            else:
                return round(sl_repayment, 2)  # Return ANNUAL amount

        except ValueError, error_message:
            print error_message
            return False

    def print_tax_ticket(self, salary, plan):
        paye = self.calculate_paye(salary, True)
        eeni = self.calculate_employee_ni(salary)
        erni = self.calculate_employer_ni(salary)
        sl = self.calculate_student_loans(salary, plan)
        net_pay_monthly = (salary / 12) - paye - sl - eeni

        print
        print("Tax Receipt for tax year {}".format(self.tax_table['tax-year']))
        print("------------------------------------------")
        print("Gross Annual Pay                 : £{:10,.2f}".format(salary))
        print("Gross Monthly Pay                : £{:10,.2f}".format(salary / 12))
        print("PAYE                   (monthly) : £{:10,.2f}".format(paye))
        print("Student Loans PLAN {}   (monthly) : £{:10,.2f}".format(plan, sl))
        print("Employee NI            (monthly) : £{:10,.2f}".format(eeni))
        print("Employer NI            (monthly) : £{:10,.2f}".format(erni))
        print("------------------------------------------")
        print("Net Monthly Pay        (monthly) : £{:10,.2f}".format(net_pay_monthly))
        print("------------------------------------------")
        print("Total Tax              (monthly) : £{:10,.2f}\n".format(paye + eeni + erni + sl))
        print
        return


def main():
    my_tax = Taxation(full_time=True, student_loan_plan=0, hours_per_week=40, tax_year='2017-2018')
    if not my_tax.tax_table:
        print "Major fuck up"
    else:
        my_tax.print_tax_ticket(100000, my_tax.student_loan_plan)


# pass
# Tests :
#  is a year in the index, i.e.2016-2017 or 2017-2018
#  is not a year in the index e.g 2015-2016
#  is not given at all - should default to 2016-2017

if __name__ == '__main__':
    main()
