import math


class AffordabilityCalculator:

    # Class Variables
    monthly_payment: float = -1.0
    down_payment: float = -1.0
    interest_rate: float = -1.0
    loan_term: float = -1.0
    home_affordability_price: int = -1

    # Getters
    def get_monthly_payment(self) -> float:
        return self.monthly_payment

    def get_down_payment(self) -> float:
        return self.down_payment

    def get_interest_rate(self) -> float:
        return self.interest_rate

    def get_loan_term(self) -> float:
        return self.loan_term

    def get_home_affordability_price(self) -> int:
        return self.home_affordability_price

    # Setters
    def set_monthly_payment(self, monthly_payment):
        self.monthly_payment = monthly_payment

    def set_down_payment(self, down_payment):
        self.down_payment = down_payment

    def set_interest_rate(self, interest_rate):
        self.interest_rate = interest_rate

    def set_loan_term(self, loan_term):
        self.loan_term = loan_term

    def set_home_affordability_price(self, home_affordability_price):
        self.home_affordability_price = home_affordability_price

    def reset_class_variables(self):
        """
        Use this function to reset the class variables before repeated use of calculator.
        """
        self.set_monthly_payment(-1.0)
        self.set_down_payment(-1.0)
        self.set_interest_rate(-1.0)
        self.set_loan_term(-1.0)
        self.set_home_affordability_price(-1)

    # Variable Checking Functions
    def _user_inputs_are_valid(self) -> bool:
        """
        Use this function to verify user inputted class variables are valid.
        """
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
        """
        Ue this function to verify the home affordability price is valid.
        """
        if self.home_affordability_price == -1:
            return False
        return True

    @staticmethod
    def convert_string_number_into_float(number) -> float:
        """
        Use this function to convert a string representing a number into a float (if possible).
        """
        if not number.isdigit():
            return -1.0
        if not float(number) >= 0:
            return -1.0
        return float(number)

    # Calculation Functions
    def calculate_home_affordability_price(self) -> str:
        """
        Use this function to calculate the maximum home price that a user can afford based on the
        provided financial variables.
        """
        if self._user_inputs_are_valid() is False:
            return "Invalid User Inputs"
        numerator = self._calculate_numerator()
        denominator = self._calculate_denominator()
        loan_affordability_price = self._calculate_loan_affordability(numerator, denominator)
        home_affordability_price = loan_affordability_price + self.down_payment
        self.set_home_affordability_price(round(home_affordability_price))
        if self._home_affordability_price_is_valid() is False:
            return "Invalid Calculation From calculate_home_affordability_price() Function"
        return str(round(home_affordability_price))

    def calculate_total_home_loan_price(self) -> str:
        """
        Use this function to calculate the total cost of a home loan over the loan term.
        """
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
        """
        Use this function to calculate the loan's principal.
        """
        if self._user_inputs_are_valid() is False:
            return "Invalid User Inputs"
        if self._home_affordability_price_is_valid() is False:
            return "Invalid Calculation From calculate_home_affordability_price() Function"
        loan_principal = self.home_affordability_price - self.down_payment
        return str(round(loan_principal))

    def calculate_loan_interest(self) -> str:
        """
        Use this function to calculate the loan's interest.
        """
        if self._user_inputs_are_valid() is False:
            return "Invalid User Inputs"
        if self._home_affordability_price_is_valid() is False:
            return "Invalid Calculation From calculate_home_affordability_price() Function"
        loan_interest = float(self.calculate_total_home_loan_price()) - float(self.calculate_loan_principal())
        return str(round(loan_interest))

    # Helper Functions
    def _convert_annual_interest_rate_to_monthly_interest_rate(self):
        """
        Use this function to convert annual interest rate to monthly interest rate
        """
        return self.interest_rate / 100 / 12

    def _convert_loan_term_length_into_months(self):
        """
        Use this function to convert loan term length from years to months
        """
        return self.loan_term * 12

    def _calculate_numerator(self) -> float:
        """
        Use this function to calculate the numerator in the calculate_home_affordability_price()
        function.
        """
        interest_rate = self._convert_annual_interest_rate_to_monthly_interest_rate()
        loan_term = self._convert_loan_term_length_into_months()
        return interest_rate * math.pow((1 + interest_rate), loan_term)

    def _calculate_denominator(self) -> float:
        """
        Use this function to calculate the denominator in the calculate_home_affordability_price()
        function.
        """
        interest_rate = self._convert_annual_interest_rate_to_monthly_interest_rate()
        loan_term = self._convert_loan_term_length_into_months()
        return math.pow((1 + interest_rate), loan_term) - 1

    def _calculate_loan_affordability(self, numerator, denominator) -> float:
        """
        Use this function to calculate the loan affordability in the
        calculate_home_affordability_price() function.
        """
        return (self.monthly_payment * denominator) / numerator

    def _calculate_monthly_payment(self) -> float:
        """
        This is a helper function for calculate_total_home_loan_price that calculates an estimated
        monthly home loan payment based on provided financial variables.
        """
        if self._user_inputs_are_valid() is False or self._home_affordability_price_is_valid() is False:
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


if __name__ == "__main__":
    calculator = AffordabilityCalculator()
