import tkinter as tk
from tkinter import messagebox
import math


# Function to parse interest rate
def parse_interest_rate(interest_rate_string):
    try:
        return float(interest_rate_string) / 100 / 12
    except Exception as e:
        tk.Tk().withdraw()  # Prevents root window from appearing
        messagebox.showerror("Error", "Error Interest Rate")
    return 0.0


# Function to parse mortgage term
def parse_term(term_index):
    if term_index == 0:
        return 180  # term in months
    return 360  # term in months


# Function to parse monthly payment
def parse_monthly_payment(monthly_payment_string):
    try:
        return float(monthly_payment_string)
    except Exception as e:
        tk.Tk().withdraw()  # Prevents root window from appearing
        messagebox.showerror("Error", "Error Monthly Payment")
    return 0.0


# Function to parse down payment
def parse_down_payment(down_payment_string):
    try:
        return float(down_payment_string)
    except Exception as e:
        tk.Tk().withdraw()  # Prevents root window from appearing
        messagebox.showerror("Error", "Error Down Payment")
    return 0.0


# Function to calculate how much how you can afford based on monthly payment
def calculate_mortgage(monthly_payment, mortgage_term, interest_rate, down_payment, hoa):
    monthly_payment -= hoa

    numerator = interest_rate * math.pow((1 + interest_rate), mortgage_term)
    denominator = math.pow((1 + interest_rate), mortgage_term) - 1
    property_value = (monthly_payment * denominator) / numerator
    property_value += down_payment

    if property_value > 0:
        return round(property_value)

    return 0


# Function to calculate estimated monthly payment
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


# Function to calculate total home price
def calculate_total_home_price(house_price, annual_interest_rate, loan_term_years):
    monthly_payment = calculate_monthly_payment(house_price, annual_interest_rate, loan_term_years)
    total_payments = loan_term_years * 12
    total_price = monthly_payment * total_payments
    return total_price


def get_loan_principal(house_price):
    return house_price


def get_loan_interest(house_price, annual_interest_rate, loan_term_years):
    total_price = calculate_total_home_price(house_price, annual_interest_rate, loan_term_years)
    principal = get_loan_principal(house_price)
    loan_interest = total_price - principal
    return loan_interest