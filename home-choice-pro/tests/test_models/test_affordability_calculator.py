import pytest
from models.affordability_calculator import AffordabilityCalculator


@pytest.fixture
def calculator(): 
    return AffordabilityCalculator()


def test_getters_and_setters():
    calculator = AffordabilityCalculator()

    calculator.set_monthly_payment(1500.0)
    assert calculator.get_monthly_payment() == 1500.0

    calculator.set_down_payment(20000.0)
    assert calculator.get_down_payment() == 20000.0

    calculator.set_interest_rate(5)
    assert calculator.get_interest_rate() == 5

    calculator.set_loan_term(30)
    assert calculator.get_loan_term() == 30

    calculator.set_home_affordability_price(300000)
    assert calculator.get_home_affordability_price() == 300000


def test_reset_class_variables():
    calculator = AffordabilityCalculator()
    calculator.set_monthly_payment(1500.0)
    calculator.set_down_payment(20000.0)
    calculator.set_interest_rate(5)
    calculator.set_loan_term(30)
    calculator.set_home_affordability_price(300000)

    calculator.reset_class_variables()

    assert calculator.get_monthly_payment() == -1.0
    assert calculator.get_down_payment() == -1.0
    assert calculator.get_interest_rate() == -1.0
    assert calculator.get_loan_term() == -1.0
    assert calculator.get_home_affordability_price() == -1


def test_user_inputs_are_valid():
    calculator = AffordabilityCalculator()
    calculator.set_monthly_payment(1500.0)
    calculator.set_down_payment(30000.0)
    calculator.set_interest_rate(3.5)
    calculator.set_loan_term(30)

    assert calculator._user_inputs_are_valid() == True

    calculator.set_monthly_payment(-1.0)
    assert calculator._user_inputs_are_valid() == False


def test_home_affordability_price_is_valid():
    calculator = AffordabilityCalculator()
    calculator.set_home_affordability_price(300000)

    assert calculator._home_affordability_price_is_valid() == True

    calculator.set_home_affordability_price(-1)
    assert calculator._home_affordability_price_is_valid() == False


def test_convert_string_number_into_float():
    assert AffordabilityCalculator.convert_string_number_into_float("1000") == 1000.0
    assert AffordabilityCalculator.convert_string_number_into_float("-1000") == -1.0
    assert AffordabilityCalculator.convert_string_number_into_float("abc") == -1.0


def test_calculate_home_affordability_price():
    calculator = AffordabilityCalculator()
    calculator.set_monthly_payment(1500.0)
    calculator.set_down_payment(20000.0)
    calculator.set_interest_rate(5)
    calculator.set_loan_term(30)

    result = calculator.calculate_home_affordability_price()
    assert result != "Invalid User Inputs"
    assert result != "Invalid Calculation From calculate_home_affordability_price() Function"
    assert calculator.calculate_home_affordability_price() == "299422"


def test_calculate_total_home_loan_price():
    calculator = AffordabilityCalculator()
    calculator.set_monthly_payment(1500.0)
    calculator.set_down_payment(20000.0)
    calculator.set_interest_rate(5)
    calculator.set_loan_term(30)
    calculator.calculate_home_affordability_price()

    result = calculator.calculate_total_home_loan_price()
    assert result != "Invalid User Inputs"
    assert result != "Invalid Calculation From calculate_home_affordability_price() Function"
    assert result != "Invalid Calculation From _calculate_monthly_payment() Function"
    assert calculator.calculate_total_home_loan_price() == "539999"


def test_calculate_loan_principal():
    calculator = AffordabilityCalculator()
    calculator.set_monthly_payment(1500.0)
    calculator.set_down_payment(20000.0)
    calculator.set_interest_rate(5)
    calculator.set_loan_term(30)
    calculator.calculate_home_affordability_price()

    result = calculator.calculate_loan_principal()
    assert result != "Invalid User Inputs"
    assert result != "Invalid Calculation From calculate_home_affordability_price() Function"
    assert calculator.calculate_loan_principal() == "279422"


def test_calculate_loan_interest():
    calculator = AffordabilityCalculator()
    calculator.set_monthly_payment(1500.0)
    calculator.set_down_payment(20000.0)
    calculator.set_interest_rate(5)
    calculator.set_loan_term(30)
    calculator.calculate_home_affordability_price()

    result = calculator.calculate_loan_interest()
    assert result != "Invalid User Inputs"
    assert result != "Invalid Calculation From calculate_home_affordability_price() Function"
    assert calculator.calculate_loan_interest() == "260577"


def test_calculate_numerator():
    calculator = AffordabilityCalculator()
    calculator.set_interest_rate(0.035)
    calculator.set_loan_term(30)

    result = calculator._calculate_numerator()
    assert isinstance(result, float)


def test_calculate_denominator():
    calculator = AffordabilityCalculator()
    calculator.set_interest_rate(0.035)
    calculator.set_loan_term(30)

    result = calculator._calculate_denominator()
    assert isinstance(result, float)


def test_calculate_loan_affordability():
    calculator = AffordabilityCalculator()
    calculator.set_monthly_payment(1500.0)
    numerator = 0.035 * (1 + 0.035) ** 30
    denominator = (1 + 0.035) ** 30 - 1

    result = calculator._calculate_loan_affordability(numerator, denominator)
    assert isinstance(result, float)
    

def test_calculate_monthly_payment():
    calculator = AffordabilityCalculator()
    calculator.set_monthly_payment(1500.0)
    calculator.set_down_payment(30000.0)
    calculator.set_interest_rate(0.035)
    calculator.set_loan_term(30)
    calculator.calculate_home_affordability_price()

    result = calculator._calculate_monthly_payment()
    assert isinstance(result, float)