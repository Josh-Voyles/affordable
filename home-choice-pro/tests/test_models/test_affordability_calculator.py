import pytest
from models.affordability_calculator import AffordabilityCalculator


@pytest.fixture
def calculator():
    return AffordabilityCalculator()

@pytest.fixture
def zero_interest_calculator():
    return AffordabilityCalculator()

def test_calculate_home_affordability_price(calculator):
    calculator.process_affordability(1500.0, 20000.0, 5, 30, 50, 1.5, 0.75, 0.85)
    assert calculator.get_max_home_price() == 197638
    assert calculator.get_total_loan_cost() == 343296
    assert calculator.get_total_loan_principal() == 177638
    assert calculator.get_total_loan_interest() == 165658

def test_calculate_home_affordability_price_with_zero_interest(zero_interest_calculator):
    zero_interest_calculator.process_affordability(1500.0, 20000.0, 0, 30, 50, 1.5, 0.75, 0.85)
    assert zero_interest_calculator.get_max_home_price() == 283471

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

