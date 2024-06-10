import math


class AffordabilityCalculator:

    # Class Variables
    monthly_payment: float
    down_payment: float
    interest_rate: float
    loan_term: float
    home_affordability_price: int

    # Constructor
    def __init__(self, monthly_payment: str, down_payment: str, interest_rate: str, loan_term: str):
        """Initializes class variables."""
        self.monthly_payment = self.convert_string_number_into_float(monthly_payment)
        self.down_payment = self.convert_string_number_into_float(down_payment)
        self.interest_rate = self.convert_string_number_into_float(interest_rate)
        self.loan_term = self.convert_string_number_into_float(loan_term)

    # Variable Checking Functions
    def _user_inputs_are_valid(self) -> bool:
        """Verifies user inputted class variables are valid."""
        class_variables = [
            self.monthly_payment,
            self.down_payment,
            self.interest_rate,
            self.loan_term
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
    def test_calculate_home_affordability_price_with_zero_interest(zero_interest_calculator):
        result = zero_interest_calculator.calculate_home_affordability_price()
        assert result != "Invalid User Inputs"
        assert result == "560000"

    def calculate_home_affordability_price(self) -> str:
        """Calculates the maximum home price that a user can afford."""
        if not self._user_inputs_are_valid():
            return "Invalid User Inputs"
        if self.interest_rate == 0:
            loan_term_months = self._convert_loan_term_length_into_months()
            loan_affordability_price = self.monthly_payment * loan_term_months
        else:
            numerator = self._calculate_numerator()
            denominator = self._calculate_denominator()
            loan_affordability_price = self._calculate_loan_affordability(numerator, denominator)
        home_affordability_price = loan_affordability_price + self.down_payment
        self.home_affordability_price = round(home_affordability_price)
        return str(round(home_affordability_price))

    def calculate_total_home_loan_price(self) -> str:
        """Calculates the total cost of a home loan over the loan term."""
        monthly_payment = self._calculate_monthly_payment()
        total_home_loan_price = monthly_payment * self._convert_loan_term_length_into_months()
        return str(round(total_home_loan_price))

    def calculate_loan_principal(self) -> str:
        """Calculates the loan's principal."""
        loan_principal = self.home_affordability_price - self.down_payment
        return str(round(loan_principal))

    def calculate_loan_interest(self) -> str:
        """Calculates the loan's interest."""
        total_home_loan_price = float(self.calculate_total_home_loan_price())
        loan_principal = float(self.calculate_loan_principal())
        loan_interest = total_home_loan_price - loan_principal
        return str(round(loan_interest))

    # Helper Functions
    def _convert_annual_interest_rate_to_monthly_interest_rate(self):
        """Converts annual interest rate to monthly interest rate."""
        return self.interest_rate / 100 / 12

    def _convert_loan_term_length_into_months(self):
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
        return (self.monthly_payment * denominator) / numerator

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
