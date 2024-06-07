import pytest
from models.affordability_calculator import AffordabilityCalculator

@pytest.fixture
def calculator(): 
    return AffordabilityCalculator()

def test_parse_interest_rate(calculator):
    assert calculator.parse_interest_rate("5.0") == pytest.approx(0.004166666666666667)
    assert calculator.parse_interest_rate("12") == pytest.approx(0.01)
    assert calculator.parse_interest_rate("0") == pytest.approx(0.0)

def test_parse_interest_rate_failure(calculator):
    with pytest.raises(ValueError):
        calculator.parse_interest_rate("abc")

def test_parse_term(calculator):
    assert calculator.parse_term(0) == 180
    assert calculator.parse_term(1) == 360
    assert calculator.parse_term(2) == 360  # any non-zero index should return 360

def test_parse_monthly_payment(calculator):
    assert calculator.parse_monthly_payment("1500") == pytest.approx(1500.0)
    assert calculator.parse_monthly_payment("0") == pytest.approx(0.0)

def test_parse_monthly_payment_failure(calculator):
    with pytest.raises(ValueError):
        calculator.parse_monthly_payment("abc") == pytest.approx(0.0)

def test_parse_down_payment(calculator):
    assert calculator.parse_down_payment("20000") == pytest.approx(20000.0)
    assert calculator.parse_down_payment("0") == pytest.approx(0.0)

def test_parse_down_payment_failure(calculator):
    with pytest.raises(ValueError):
        calculator.parse_down_payment("abc") == pytest.approx(0.0)

def test_calculate_home_affordability(calculator):
    assert calculator.calculate_home_affordability(1500, 360, 0.004166666666666667, 20000) == 299422
    assert calculator.calculate_home_affordability(1500, 180, 0.004166666666666667, 20000) == 209683
    assert calculator.calculate_home_affordability(0, 360, 0.004166666666666667, 20000) == 20000

def test_calculate_monthly_payment(calculator):
    assert calculator.calculate_monthly_payment(400000, 5, 30, 20000) == pytest.approx(2147.29, 0.01)
    assert calculator.calculate_monthly_payment(300000, 3.5, 15, 50000) == pytest.approx(1785.91, 0.01)
    assert calculator.calculate_monthly_payment(200000, 0, 30, 50000) == pytest.approx(416.67, 0.01)

def test_calculate_total_home_loan_price(calculator):
    assert calculator.calculate_total_home_loan_price(400000, 5, 30, 20000) == pytest.approx(773024.40, 0.01)
    assert calculator.calculate_total_home_loan_price(300000, 3.5, 15, 50000) == pytest.approx(321464.20, 0.01)

def test_get_loan_principal(calculator):
    assert calculator.get_loan_principal(400000, 20000) == 380000
    assert calculator.get_loan_principal(300000, 50000) == 250000

def test_get_loan_interest(calculator):
    assert calculator.get_loan_interest(400000, 5, 30, 20000) == pytest.approx(393024.40, 0.01)
    assert calculator.get_loan_interest(300000, 3.5, 15, 50000) == pytest.approx(71464.20, 0.01)
