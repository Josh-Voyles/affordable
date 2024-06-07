import tkinter as tk
from tkinter import messagebox
import math


# Parsing Functions
# Parse interest rate
def parse_interest_rate(interest_rate_string):
    try:
        return float(interest_rate_string) / 100 / 12
    except Exception as e:
        tk.Tk().withdraw()  # Prevents root window from appearing
        messagebox.showerror("Error", "Error Interest Rate")
    return 0.0


# Parse mortgage term
def parse_term(term_index):
    if term_index == 0:
        return 180  # term in months
    return 360  # term in months


# Parse monthly payment
def parse_monthly_payment(monthly_payment_string):
    try:
        return float(monthly_payment_string)
    except Exception as e:
        tk.Tk().withdraw()  # Prevents root window from appearing
        messagebox.showerror("Error", "Error Monthly Payment")
    return 0.0


# Parse down payment
def parse_down_payment(down_payment_string):
    try:
        return float(down_payment_string)
    except Exception as e:
        tk.Tk().withdraw()  # Prevents root window from appearing
        messagebox.showerror("Error", "Error Down Payment")
    return 0.0


# Calculation Functions
# Calculate how much home user can afford based on desired monthly payment
def calculate_home_affordability(monthly_payment, mortgage_term, interest_rate, down_payment):
    numerator = interest_rate * math.pow((1 + interest_rate), mortgage_term)
    denominator = math.pow((1 + interest_rate), mortgage_term) - 1
    property_value = (monthly_payment * denominator) / numerator
    property_value += down_payment

    if property_value > 0:
        return round(property_value)

    return 0


# Calculate estimated monthly payment of a home loan
def calculate_monthly_payment(house_price, annual_interest_rate, loan_term_years, down_payment):
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


# Calculate total home loan price
def calculate_total_home_loan_price(house_price, annual_interest_rate, loan_term_years, down_payment):
    monthly_payment = calculate_monthly_payment(house_price, annual_interest_rate, loan_term_years, down_payment)
    total_payments = loan_term_years * 12
    total_price = monthly_payment * total_payments
    return total_price


# Getter Functions
# Get home loan principal amount
def get_loan_principal(house_price, down_payment):
    return house_price - down_payment


# Get home loan interest amount
def get_loan_interest(house_price, annual_interest_rate, loan_term_years, down_payment):
    total_price = calculate_total_home_loan_price(house_price, annual_interest_rate, loan_term_years, down_payment)
    principal = get_loan_principal(house_price, down_payment)
    loan_interest = total_price - principal
    return loan_interest

# Test variables
interest_rate_string = "5.0"
term_index = 0
monthly_payment_string = "1500"
down_payment_string = "20000"
hoa_fee = 100

# Test parsing functions
parsed_interest_rate = parse_interest_rate(interest_rate_string)
parsed_term = parse_term(term_index)
parsed_monthly_payment = parse_monthly_payment(monthly_payment_string)
parsed_down_payment = parse_down_payment(down_payment_string)

# Output parsed values
print(f"Parsed Interest Rate: {parsed_interest_rate}")
print(f"Parsed Term: {parsed_term}")
print(f"Parsed Monthly Payment: {parsed_monthly_payment}")
print(f"Parsed Down Payment: {parsed_down_payment}")

# Test calculation functions
home_affordability = calculate_home_affordability(parsed_monthly_payment, parsed_term, parsed_interest_rate, parsed_down_payment)
monthly_payment = calculate_monthly_payment(300000, 5, 30, 20000)
total_home_loan_price = calculate_total_home_loan_price(300000, 5, 30, 20000)

# Output calculation results
print(f"Home Affordability: {home_affordability}")
print(f"Estimated Monthly Payment: {monthly_payment}")
print(f"Total Home Loan Price: {total_home_loan_price}")

# Test getter functions
loan_principal = get_loan_principal(300000, 20000)
loan_interest = get_loan_interest(300000, 5, 30, 20000)

# Output getter results
print(f"Loan Principal: {loan_principal}")
print(f"Loan Interest: {loan_interest}")
