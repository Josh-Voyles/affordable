import math

class AffordabilityCalculator:

    def parse_interest_rate(self, interest_rate_string):
        try:
            return float(interest_rate_string) / 100 / 12
        except ValueError:
            raise ValueError("Error Interest Rate")

    def parse_term(self, term_index):
        if term_index == 0:
            return 180  # term in months
        return 360  # term in months

    def parse_monthly_payment(self, monthly_payment_string):
        try:
            return float(monthly_payment_string)
        except ValueError:
            raise ValueError("Error Monthly Payment")

    def parse_down_payment(self, down_payment_string):
        try:
            return float(down_payment_string)
        except ValueError:
            raise ValueError("Error Down Payment")

    def calculate_home_affordability(self, monthly_payment, mortgage_term, interest_rate, down_payment):
        numerator = interest_rate * math.pow((1 + interest_rate), mortgage_term)
        denominator = math.pow((1 + interest_rate), mortgage_term) - 1
        property_value = (monthly_payment * denominator) / numerator
        property_value += down_payment

        if property_value > 0:
            return round(property_value)

        return 0

    def calculate_monthly_payment(self, house_price, annual_interest_rate, loan_term_years, down_payment):
        loan_amount = house_price - down_payment
        monthly_interest_rate = annual_interest_rate / 100 / 12
        total_payments = loan_term_years * 12

        if monthly_interest_rate == 0:
            monthly_payment = loan_amount / total_payments
        else:
            monthly_payment = loan_amount * (
                        monthly_interest_rate * math.pow(1 + monthly_interest_rate, total_payments)) / (
                                          math.pow(1 + monthly_interest_rate, total_payments) - 1)

        return monthly_payment

    def calculate_total_home_loan_price(self, house_price, annual_interest_rate, loan_term_years, down_payment):
        monthly_payment = self.calculate_monthly_payment(house_price, annual_interest_rate, loan_term_years, down_payment)
        total_payments = loan_term_years * 12
        total_price = monthly_payment * total_payments
        return total_price

    def get_loan_principal(self, house_price, down_payment):
        return house_price - down_payment

    def get_loan_interest(self, house_price, annual_interest_rate, loan_term_years, down_payment):
        total_price = self.calculate_total_home_loan_price(house_price, annual_interest_rate, loan_term_years, down_payment)
        principal = self.get_loan_principal(house_price, down_payment)
        loan_interest = total_price - principal
        return loan_interest

if __name__ == "__main__":
    calculator = AffordabilityCalculator()
