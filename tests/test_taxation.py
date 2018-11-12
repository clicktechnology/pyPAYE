# coding=utf-8
import inspect
import unittest

from taxation import Taxation

# tax_object_default does not specify a date, so that the function tests the default behaviour for backwards compatibility.
tax_object_default = Taxation(full_time=True, student_loan_plan=0, hours_per_week=40)

# tax_object_2017_2018 specifies a date, so that the function runs in normal mode.
tax_object_2017_2018 = Taxation(full_time=True, student_loan_plan=0, hours_per_week=40, tax_year='2017-2018')


# https://listentotaxman.com/
# http://tools.hmrc.gov.uk/hmrctaxcalculator/screen/Personal+Tax+Calculator/en-GB/summary?user=guest

class TestCases(unittest.TestCase):
    # These are to test whether valid inputs return the correct monthly values.  The spread of inputs covers
    # every tax bracket.

    known_values_monthly = (
        (2000, 0),
        (11500, 8.33),
        (20000, 150.0),
        (35000, 400.0),
        (45000, 600.00),
        (72000, 1500.0),
        (100000, 2433.33),
        (102500, 2558.33),  # HMRC - £2,558.03 : LTT - £2,558.33
        (110500, 2958.33),  # HMRC - £2,958.03 : LTT - £2,958.33
        (120500, 3458.33),  # HMRC - £3,458.03 : LTT - £3,458.33
        (130320, 3810.67),  # HMRC - £3,810.66 : LTT - £3,810.67
        (155292, 4665.12),  # HMRC - £4,665.11 : LTT - £4,665.12
        (175890, 5437.54),  # HMRC - £5,437.54 : LTT - £5,437.54
        (210000, 6716.67),  # HMRC - £6,716.66 : LTT - £6,716.67
        (245000, 8029.17),  # HMRC - £8,029.16 : LTT - £8,029.17
        (335000, 11404.17)  # HMRC - £11,404.16 : LTT - £11,404.17
    )

    # These are to test whether valid inputs return the correct annual values.

    known_values_annual = (

        # Annual salary, PAYE, Student Loan (Plan 2), Student Loan (Plan 1)

        (6000, 0, 0, 0),
        (23000, 2400, 180, 495),
        (52000, 10000, 2790, 3105),
        (102500, 30700, 7335, 7650),
        (105000, 32200, 7560, 7875),
        (130000, 45600, 9810, 10125),
        (163000, 59450, 12780, 13095),
        (289000, 116150, 24120, 24435),
        (344000, 140900, 29070, 29385)
    )

    def test010_calculate_paye_for_known_values_monthly(self):
        """calculate_paye should give known result with known input"""

        for gross_salary, result in self.known_values_monthly:
            calculated_result = tax_object_default.calculate_paye(gross_salary, True)  # True here means monthly
            self.assertAlmostEqual(calculated_result, result, 2)

    def test020_calculate_paye_for_known_values_annual(self):
        """calculate_paye should give known result with known input"""

        for gross_salary, result, __, __ in self.known_values_annual:
            calculated_result = tax_object_default.calculate_paye(gross_salary, False)  # False here means annually
            self.assertEquals(result, calculated_result)

    def test030_calculate_paye_deltas(self):
        """calculate_paye should give known result with known input"""

        delta = 0.01

        for gross_salary, result in self.known_values_monthly:
            calculated_result = tax_object_default.calculate_paye(gross_salary, True)  # True here means monthly
            difference = abs(calculated_result - result)
            self.assertTrue(difference < delta,
                            "difference: %s is not less than %s" % (difference, delta))

    def test040_return_version(self):
        """return_version should return the current version of the Taxation class."""

        self.assertEquals('0.1.4', tax_object_default.get_version(),
                          'Version number is wrong.  It should be {}. Check the value in test {}.'.
                          format(tax_object_default.get_version(), inspect.currentframe().f_code.co_name))

    def test050_bad_inputs_calculate_employee_ni(self):
        """calculate_paye should error out with bad inputs."""

        self.assertFalse(tax_object_default.calculate_employee_ni('50,000'))
        self.assertFalse(tax_object_default.calculate_employee_ni('twenty grand'))
        self.assertFalse(tax_object_default.calculate_employee_ni(-25000))
        self.assertFalse(tax_object_default.calculate_employee_ni(14 / 256))
        self.assertFalse(tax_object_default.calculate_employee_ni(''))

    def test052_bad_inputs_calculate_employer_ni(self):
        """calculate_paye should error out with bad inputs."""

        self.assertFalse(tax_object_default.calculate_employer_ni('50,000'))
        self.assertFalse(tax_object_default.calculate_employer_ni('twenty grand'))
        self.assertFalse(tax_object_default.calculate_employer_ni(-25000))
        self.assertFalse(tax_object_default.calculate_employer_ni(14 / 256))
        self.assertFalse(tax_object_default.calculate_employer_ni(''))

    def test054_bad_inputs_paye(self):
        """calculate_paye should error out with bad inputs."""

        self.assertFalse(tax_object_default.calculate_paye('50,000'))
        self.assertFalse(tax_object_default.calculate_paye('twenty grand'))
        self.assertFalse(tax_object_default.calculate_paye(-25000))
        self.assertFalse(tax_object_default.calculate_paye(14 / 256))
        self.assertFalse(tax_object_default.calculate_paye(''))

    def test056_bad_inputs_calculate_student_loans(self):
        """calculate_paye should error out with bad inputs."""

        self.assertFalse(tax_object_default.calculate_student_loans('50,000', 1))
        self.assertFalse(tax_object_default.calculate_student_loans('twenty grand', 2))
        self.assertFalse(tax_object_default.calculate_student_loans(-25000, 3))
        self.assertFalse(tax_object_default.calculate_student_loans(14 / 256, 1))
        self.assertFalse(tax_object_default.calculate_student_loans('', 2))
        self.assertFalse(tax_object_default.calculate_student_loans(32000, 4))

    def test060_calculate_student_loan_repayments(self):
        """calculate_paye should give known result with known input"""

        for plan in [1, 2]:
            for gross_salary, __, result_plan_2, result_plan_1 in self.known_values_annual:
                calculated_result = tax_object_default.calculate_student_loans(gross_salary, plan,
                                                                               False)  # False means annual
                if plan == 1:
                    self.assertEquals(result_plan_1, calculated_result)
                elif plan == 2:
                    self.assertEquals(result_plan_2, calculated_result)

    def test070_test_is_valid_number(self):
        """Checks to see whether the is_valid_number function is working."""

        self.assertFalse(tax_object_default.is_valid_number('50,000'))
        self.assertFalse(tax_object_default.is_valid_number('0'))
        self.assertFalse(tax_object_default.is_valid_number('0.0'))
        self.assertFalse(tax_object_default.is_valid_number('-1'))
        self.assertFalse(tax_object_default.is_valid_number('-245'))
        self.assertFalse(tax_object_default.is_valid_number(''))
        self.assertTrue(tax_object_default.is_valid_number(55000))

    def test080_test_rates_dictionary(self):
        """Checks to see that the dictionary for the tay year data is correct."""

        # Test to see if bad dates get flagged : Test returns TRUE when function returns FALSE because the year
        # component of tax_year, namely 'wrong date' is not valid.
        my_tax = Taxation(full_time=True, student_loan_plan=0, hours_per_week=40, tax_year='wrong date')
        self.assertFalse(my_tax.tax_table)
        del my_tax

        # Test returns TRUE because function returns valid dictionary containing tax_year set to value '2016-2017'
        # which is the default, for the sake of backwards compatibility.
        my_tax = Taxation(full_time=True, student_loan_plan=0, hours_per_week=40)
        self.assertEquals(my_tax.tax_table['tax-year'], '2016-2017')
        del my_tax

        # Test returns TRUE because function returns valid dictionary containing tax_year set to value '2017-2018'
        # when correctly specified.  In other words, correct usage gets correct response.
        my_tax = Taxation(full_time=True, student_loan_plan=0, hours_per_week=40, tax_year='2017-2018')
        self.assertEquals(my_tax.tax_table['tax-year'], '2017-2018')
        del my_tax


if __name__ == '__main__':
    unittest.main()
