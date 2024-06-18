import pytest
from models.affordability_calculator import AffordabilityCalculator


@pytest.fixture
def calculator():
    return AffordabilityCalculator("1500.0", "20000.0", "5", "30", "50", "1.5")

@pytest.fixture
def zero_interest_calculator():
    return AffordabilityCalculator("1500.0", "20000.0", "0", "30", "50", "1.5")

@pytest.fixture
def empty_calculator_fields():
    return AffordabilityCalculator()


def test_user_inputs_are_valid(calculator):
    assert calculator._user_inputs_are_valid() == True

    calculator.monthly_payment = -1.0
    assert calculator._user_inputs_are_valid() == False


def test_convert_string_number_into_float():
    assert AffordabilityCalculator.convert_string_number_into_float("1000") == 1000.0
    assert AffordabilityCalculator.convert_string_number_into_float("-1000") == -1.0
    assert AffordabilityCalculator.convert_string_number_into_float("abc") == -1.0


def test_calculate_home_affordability_price(calculator):
    result = calculator.calculate_home_affordability_price()
    assert result != -1
    assert calculator.calculate_home_affordability_price() == 235314


def test_calculate_home_affordability_price_with_zero_interest(zero_interest_calculator):
    result = zero_interest_calculator.calculate_home_affordability_price()
    assert result != -1
    assert result == 373793


def test_empty_calculator_fields(empty_calculator_fields):
    result = empty_calculator_fields.calculate_home_affordability_price()
    assert result != -1
    assert result == 0


def test_calculate_total_home_loan_price(calculator):
    calculator.calculate_home_affordability_price()
    result = calculator.calculate_total_home_loan_price()
    assert calculator.calculate_total_home_loan_price() == 416107


def test_calculate_loan_principal(calculator):
    calculator.calculate_home_affordability_price()
    result = calculator.calculate_loan_principal()
    assert calculator.calculate_loan_principal() == 215314


def test_calculate_loan_interest(calculator):
    calculator.calculate_home_affordability_price()
    result = calculator.calculate_loan_interest()
    assert calculator.calculate_loan_interest() == 200793


def test_calculate_numerator(calculator):
    calculator.interest_rate = 3.5
    calculator.loan_term = 30.0
    result = calculator._calculate_numerator()
    assert isinstance(result, float)


def test_calculate_denominator(calculator):
    calculator.interest_rate = 0.035
    calculator.loan_term = 30
    result = calculator._calculate_denominator()
    assert isinstance(result, float)


def test_calculate_loan_affordability(calculator):
    numerator = 0.035 * (1 + 0.035) ** 30
    denominator = (1 + 0.035) ** 30 - 1
    result = calculator._calculate_loan_affordability(numerator, denominator)
    assert isinstance(result, float)


def test_calculate_monthly_payment(calculator):
    calculator.calculate_home_affordability_price()
    result = calculator._calculate_monthly_mortgage_payment()
    assert isinstance(result, float)
