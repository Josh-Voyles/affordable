import pytest
from models.affordability_calculator import AffordabilityCalculator


@pytest.fixture
def calculator():
    return AffordabilityCalculator()


@pytest.fixture
def zero_interest_calculator():
    return AffordabilityCalculator()


def test_process_affordability(calculator):
    calculator.process_affordability(1500.0, 20000.0, 5, 30, 50, 1.5, 0.75, 0.85)
    assert calculator.get_max_home_price() == 197638
    assert calculator.get_total_loan_cost() == 343296
    assert calculator.get_total_loan_principal() == 177638
    assert calculator.get_total_loan_interest() == 165658


def test_process_affordability_with_zero_interest(zero_interest_calculator):
    zero_interest_calculator.process_affordability(1500.0, 20000.0, 0, 30, 50, 1.5, 0.75, 0.85)
    assert zero_interest_calculator.get_max_home_price() == 283471


def test_calculate_max_home_price(calculator):
    calculator.process_affordability(1500.0, 20000.0, 5, 30, 50, 1.5, 0.75, 0.85)
    assert calculator.get_max_home_price() == 197638


def test_calculate_total_loan_price(calculator):
    calculator.process_affordability(1500.0, 20000.0, 5, 30, 50, 1.5, 0.75, 0.85)
    assert calculator.get_total_loan_cost() == 343296
    assert calculator.get_total_loan_principal() == 177638


def test_calculate_total_loan_principal(calculator):
    calculator.process_affordability(1500.0, 20000.0, 5, 30, 50, 1.5, 0.75, 0.85)
    assert calculator.get_total_loan_principal() == 177638


def test_calculate_loan_interest(calculator):
    calculator.process_affordability(1500.0, 20000.0, 5, 30, 50, 1.5, 0.75, 0.85)
    assert calculator.get_total_loan_interest() == 165658


def test_adjust_for_property_taxes_and_insurance(calculator):
    monthly_payment = 1500.0 - 50  # desired monthly payment minus monthly HOA fees
    interest_rate = 5 / 100 / 12
    loan_term = 30 * 12
    property_tax = 1.5 / 100 / 12
    house_insurance = 0.75 / 100 / 12
    pmi = 0.85 / 100
    result = calculator._adjust_for_property_taxes_and_insurance(
        monthly_payment,
        299422,
        20000.0,
        interest_rate,
        loan_term,
        property_tax,
        50,
        house_insurance,
        pmi,)
    assert f"{result:.2f}" == "197638.00"


def test_calculate_monthly_pmi(calculator):
    pmi = 0.85 / 100
    result = calculator._calculate_monthly_pmi_payment(
        299422.0,
        20000.0,
        pmi
    )
    assert f"{result:.2f}" == "197.92"


def test_calculate_monthly_mortgage_payment(calculator):
    interest_rate = 5 / 100 / 12
    loan_term = 30 * 12
    result = calculator._calculate_monthly_mortgage_payment(
        299422.0,
        20000.0,
        interest_rate,
        loan_term
    )
    assert f"{result:.2f}" == "1500.00"


def test_calculate_numerator(calculator):
    interest_rate = 6.125 / 100 / 12
    loan_term = 30 * 12
    result = calculator._calculate_numerator(interest_rate, loan_term)
    assert f"{result:.2f}" == "0.03"


def test_calculate_denominator(calculator):
    interest_rate = 6.125 / 100 / 12
    loan_term = 30 * 12
    result = calculator._calculate_denominator(interest_rate, loan_term)
    assert f"{result:.2f}" == "5.25"

