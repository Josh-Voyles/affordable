"""
Home Choice Pro Morgtage Calculator

This application calculates 'how much house you can afford' based on monthly payment.

UMGC CMSC 495 6380
Class Project
Joey Garcia
Josh Voyles
Randy Shreeves
Zaria Gibbs

Main logic class behind calculating house price based on monthly payment

"""

import math


class AffordabilityCalculator:
    '''Calculates the afforadibility based on financial parameters'''

    # Class Variables
    monthly_payment: float
    down_payment: float
    interest_rate: float
    loan_term: float
    home_affordability_price: int
    hoa_monthly_fee: float

    # Constructor
    def __init__(self, monthly_payment: str = "0", down_payment: str = "0",
                 interest_rate: str = "0", loan_term: str = "0", hoa_monthly_fee: str = "0"):
        """Initializes class variables."""
        self.monthly_payment = self.convert_string_number_into_float(monthly_payment)
        self.down_payment = self.convert_string_number_into_float(down_payment)
        self.interest_rate = self.convert_string_number_into_float(interest_rate)
        self.loan_term = self.convert_string_number_into_float(loan_term)
        self.hoa_monthly_fee = self.convert_string_number_into_float(hoa_monthly_fee)

    # Variable Checking Functions
    def _user_inputs_are_valid(self) -> bool:
        """Verifies user inputted class variables are valid."""
        class_variables = [
            self.monthly_payment,
            self.down_payment,
            self.interest_rate,
            self.loan_term,
            self.hoa_monthly_fee
        ]
        if any(var == -1.0 for var in class_variables):
            return False
        return True

    @staticmethod
    def convert_string_number_into_float(number) -> float:
        """Converts a string representing a number into a float (if possible)."""
        try:
            parsed_number = float(number)
            if parsed_number >= 0:
                return parsed_number
            return -1.0
        except ValueError:
            return -1.0

    # Calculation Functions
    def calculate_home_affordability_price(self) -> int:
        """Calculates the maximum home price that a user can afford."""
        if not self._user_inputs_are_valid():
            return -1
        numerator = self._calculate_numerator()
        denominator = self._calculate_denominator()
        loan_affordability_price = self._calculate_loan_affordability(numerator, denominator)
        home_affordability_price = loan_affordability_price + self.down_payment
        self.home_affordability_price = round(home_affordability_price)
        return round(home_affordability_price)

    def calculate_total_home_loan_price(self) -> int:
        """Calculates the total cost of a home loan over the loan term."""
        monthly_payment = self._calculate_monthly_payment()
        total_home_loan_price = monthly_payment * self._convert_loan_term_length_into_months()
        return round(total_home_loan_price)

    def calculate_loan_principal(self) -> int:
        """Calculates the loan's principal."""
        loan_principal = self.home_affordability_price - self.down_payment
        return round(loan_principal)

    def calculate_loan_interest(self) -> int:
        """Calculates the loan's interest."""
        total_home_loan_price = float(self.calculate_total_home_loan_price())
        loan_principal = float(self.calculate_loan_principal())
        loan_interest = total_home_loan_price - loan_principal
        return round(loan_interest)

    # Helper Functions
    def _convert_annual_interest_rate_to_monthly_interest_rate(self) -> float:
        """Converts annual interest rate to monthly interest rate."""
        return self.interest_rate / 100 / 12

    def _convert_loan_term_length_into_months(self) -> float:
        """Converts loan term length from years to months."""
        return self.loan_term * 12

    def _calculate_numerator(self) -> float:
        """Helper function for the calculate_home_affordability_price() function."""
        interest_rate = self._convert_annual_interest_rate_to_monthly_interest_rate()
        loan_term = self._convert_loan_term_length_into_months()
        return interest_rate * math.pow((1 + interest_rate), loan_term)

    def _calculate_denominator(self) -> float:
        """Helper function for the calculate_home_affordability_price() function."""
        interest_rate = self._convert_annual_interest_rate_to_monthly_interest_rate()
        loan_term = self._convert_loan_term_length_into_months()
        return math.pow((1 + interest_rate), loan_term) - 1

    def _calculate_loan_affordability(self, numerator, denominator) -> float:
        """Helper function for the calculate_home_affordability_price() function."""
        monthly_payment = self.monthly_payment - self.hoa_monthly_fee
        if monthly_payment < 0:  # Desired monthly payment can't be less than monthly HOA fees
            return -1
        loan_term = self._convert_loan_term_length_into_months()
        if numerator == 0:  # Numerator is 0 if interest rate inputted was 0%
            return monthly_payment * loan_term
        return (monthly_payment * denominator) / numerator  # If interest rate > 0%, return this

    def _calculate_monthly_payment(self) -> float:
        """Helper function for the calculate_total_home_loan_price() function."""
        loan_amount = self.home_affordability_price - self.down_payment
        interest_rate = self._convert_annual_interest_rate_to_monthly_interest_rate()
        loan_term = self._convert_loan_term_length_into_months()
        if interest_rate == 0:
            monthly_payment = loan_amount / loan_term
        else:
            monthly_payment = loan_amount * (
                        interest_rate * math.pow(1 + interest_rate, loan_term)) / (
                                          math.pow(1 + interest_rate, loan_term) - 1)
        return monthly_payment
