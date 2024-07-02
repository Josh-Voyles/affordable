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
    """Calculates the affordability based on financial parameters"""

    # Constructor
    def __init__(self):
        """Initializes class variables."""
        # to return
        self._max_home_price: int = 0
        self._total_loan_cost: int = 0
        self._total_loan_principal: int = 0
        self._total_loan_interest: int = 0

    def get_max_home_price(self) -> int:
        return self._max_home_price

    def get_total_loan_cost(self) -> int:
        return self._total_loan_cost

    def get_total_loan_principal(self) -> int:
        return self._total_loan_principal

    def get_total_loan_interest(self) -> int:
        return self._total_loan_interest

    def process_affordability(
        self,
        monthly_payment,
        down_payment,
        interest_rate,
        loan_term,
        hoa_monthly,
        property_tax,
        house_insurance,
        pmi,
    ) -> int:

        # convert to needed format
        interest_rate = interest_rate / 100 / 12  # convert to monthly
        loan_term = loan_term * 12
        property_tax = property_tax / 100 / 12
        house_insurance = house_insurance / 100 / 12
        pmi = pmi / 100  # monthly converter later

        self._max_home_price = self._calculate_max_home_price(
            monthly_payment,
            down_payment,
            interest_rate,
            loan_term,
            hoa_monthly,
            property_tax,
            house_insurance,
            pmi,
        )
        self._total_loan_cost = self._calculate_total_loan_price(
            self._max_home_price, down_payment, interest_rate, loan_term
        )
        self._total_loan_principal = self._calculate_total_loan_principal(
            self._max_home_price, down_payment
        )
        self._total_loan_interest = self._calculate_loan_interest(
            self._max_home_price, down_payment, interest_rate, loan_term
        )

    # Calculation Functions
    def _calculate_max_home_price(
        self,
        monthly_payment,
        down_payment,
        interest_rate,
        loan_term,
        hoa_monthly,
        property_tax,
        house_insurance,
        pmi,
    ) -> int:
        """Calculates the maximum home price that a user can afford."""
        numerator = self._calculate_numerator(interest_rate, loan_term)
        denominator = self._calculate_denominator(interest_rate, loan_term)

        monthly_payment = monthly_payment - hoa_monthly

        if monthly_payment < 0:
            return 0  # not a possible scenario, so zero
        elif numerator == 0:
            max_home_price = monthly_payment * loan_term  # mythical zero interest loan
        else:
            max_home_price = (monthly_payment * denominator) / numerator  # normal loan

        max_home_price = round(max_home_price + down_payment)

        max_home_price = self._adjust_for_property_taxes_and_insurance(
            monthly_payment,
            max_home_price,
            down_payment,
            interest_rate,
            loan_term,
            property_tax,
            hoa_monthly,
            house_insurance,
            pmi,
        )

        return round(max_home_price)

    def _calculate_total_loan_price(
        self, max_home_price, down_payment, interest_rate, loan_term
    ) -> int:
        """Calculates the total cost of a home loan over the loan term."""
        monthly_payment = self._calculate_monthly_mortgage_payment(
            max_home_price, down_payment, interest_rate, loan_term
        )
        total_home_loan_price = monthly_payment * loan_term
        return round(total_home_loan_price)

    def _calculate_total_loan_principal(self, max_home_price, down_payment) -> int:
        """Calculates the loan's principal."""
        loan_principal = max_home_price - down_payment
        return round(loan_principal)

    def _calculate_loan_interest(
        self, max_home_price, down_payment, interest_rate, loan_term
    ) -> int:
        """Calculates the loan's interest."""
        total_home_loan_price = self._calculate_total_loan_price(
            max_home_price, down_payment, interest_rate, loan_term
        )
        loan_principal = self._calculate_total_loan_principal(
            max_home_price, down_payment
        )
        loan_interest = total_home_loan_price - loan_principal
        return round(loan_interest)

    def _adjust_for_property_taxes_and_insurance(
        self,
        monthly_payment,
        max_home_price,
        down_payment,
        interest_rate,
        loan_term,
        property_tax,
        hoa_monthly,
        house_insurance,
        pmi,
    ) -> int:
        """Helper function to factor property taxes into home affordability price."""
        while True:
            monthly_tax_payment = max_home_price * property_tax
            monthly_insurance_payment = max_home_price * house_insurance
            monthly_pmi_payment = self._calculate_monthly_pmi_payment(
                max_home_price, down_payment, pmi
            )

            estimated_monthly_payment = (
                self._calculate_monthly_mortgage_payment(
                    max_home_price, down_payment, interest_rate, loan_term
                )
                + monthly_tax_payment
                + monthly_insurance_payment
                + monthly_pmi_payment
            )
            if estimated_monthly_payment <= monthly_payment:
                return max_home_price
            max_home_price -= 1

    def _calculate_monthly_pmi_payment(
        self, max_home_price, down_payment, pmi
    ) -> float:
        """Helper function to factor PMI percentage into home affordability price."""
        loan_amount = self._calculate_total_loan_principal(max_home_price, down_payment)
        if loan_amount == 0 or max_home_price == 0:
            return 0.0
        loan_to_value_ratio = loan_amount / max_home_price
        if loan_to_value_ratio <= 0.8:
            return 0.0
        annual_premium = loan_amount * pmi
        monthly_premium = annual_premium / 12
        return monthly_premium

    def _calculate_monthly_mortgage_payment(
        self, max_home_price, down_payment, interest_rate, loan_term
    ) -> float:
        """Helper function for the _calculate_total_loan_price() function."""
        loan_amount = max_home_price - down_payment
        if interest_rate == 0:
            monthly_payment = loan_amount / loan_term
        else:
            numerator = self._calculate_numerator(interest_rate, loan_term)
            denominator = self._calculate_denominator(interest_rate, loan_term)
            monthly_payment = loan_amount * numerator / denominator
        return monthly_payment

    def _calculate_numerator(self, interest_rate, loan_term) -> float:
        """Helper function for the calculate_max_home_price() function."""
        return interest_rate * math.pow((1 + interest_rate), loan_term)

    def _calculate_denominator(self, interest_rate, loan_term) -> float:
        """Helper function for the calculate_max_home_price() function."""
        return math.pow((1 + interest_rate), loan_term) - 1
