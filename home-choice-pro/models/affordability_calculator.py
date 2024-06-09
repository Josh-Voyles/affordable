import math


class AffordabilityCalculator:

    # Class Variables
    monthly_payment: float
    down_payment: float
    interest_rate: float
    loan_term: float
    home_affordability_price: int

    # Constructor
    def __init__(self, monthly_payment, down_payment, interest_rate, loan_term):
        """Initializes class variables."""
        self.monthly_payment = monthly_payment
        self.down_payment = down_payment
        self.interest_rate = interest_rate
        self.loan_term = loan_term
        # Default value for uninitialized home affordability price
        self.home_affordability_price = -1

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

    def _home_affordability_price_is_valid(self) -> bool:
        """Verifies the home affordability price is valid."""
        if self.home_affordability_price == -1:
            return False
        return True

    @staticmethod
    def convert_string_number_into_float(number) -> float:
        """Converts a string representing a number into a float (if possible)."""
        if not number.isdigit():
            return -1.0
        if not float(number) >= 0:
            return -1.0
        return float(number)

    # Calculation Functions
    def calculate_home_affordability_price(self) -> str:
        """Calculates the maximum home price that a user can afford."""
        if self._user_inputs_are_valid() is False:
            return "Invalid User Inputs"
        numerator = self._calculate_numerator()
        denominator = self._calculate_denominator()
        loan_affordability_price = self._calculate_loan_affordability(numerator, denominator)
        home_affordability_price = loan_affordability_price + self.down_payment
        self.home_affordability_price = round(home_affordability_price)
        if self._home_affordability_price_is_valid() is False:
            return "Invalid Calculation From calculate_home_affordability_price() Function"
        return str(round(home_affordability_price))

    def calculate_total_home_loan_price(self) -> str:
        """Calculates the total cost of a home loan over the loan term."""
        if self._user_inputs_are_valid() is False:
            return "Invalid User Inputs"
        if self._home_affordability_price_is_valid() is False:
            return "Invalid Calculation From calculate_home_affordability_price() Function"
        monthly_payment = self._calculate_monthly_payment()
        if monthly_payment < 0:
            return "Invalid Calculation From _calculate_monthly_payment() Function"
        total_home_loan_price = monthly_payment * self._convert_loan_term_length_into_months()
        return str(round(total_home_loan_price))

    def calculate_loan_principal(self) -> str:
        """Calculates the loan's principal."""
        if self._user_inputs_are_valid() is False:
            return "Invalid User Inputs"
        if self._home_affordability_price_is_valid() is False:
            return "Invalid Calculation From calculate_home_affordability_price() Function"
        loan_principal = self.home_affordability_price - self.down_payment
        return str(round(loan_principal))

    def calculate_loan_interest(self) -> str:
        """Calculates the loan's interest."""
        if self._user_inputs_are_valid() is False:
            return "Invalid User Inputs"
        if self._home_affordability_price_is_valid() is False:
            return "Invalid Calculation From calculate_home_affordability_price() Function"
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
        if self._user_inputs_are_valid() is False \
                or self._home_affordability_price_is_valid() is False:
            return -1.0
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
