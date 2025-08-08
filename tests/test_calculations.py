import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFundsError

@pytest.fixture
def zero_bank_account():
    """Fixture to create a bank account with zero balance."""
    print("Creating a bank account with zero balance")
    return BankAccount(0.0)

@pytest.fixture
def bank_account_with_balance():
    """Fixture to create a bank account with a specific balance."""
    print("Creating a bank account with a balance of 100.0")
    return BankAccount(100.0)


@pytest.mark.parametrize(
    "num1, num2, expected",
    [
        (2, 3, 5),
        (-1, 1, 0),
        (0, 0, 0),
        (100, 200, 300),
        (-50, -50, -100),
        (123456789, 987654321, 1111111110),
    ])
def test_add(num1, num2, expected):
    """Test the add function."""
    assert add(num1, num2) == expected


def test_subtract():
    """Test the subtract function."""
    assert subtract(5, 3) == 2
    assert subtract(0, 0) == 0
    assert subtract(-1, -1) == 0

def test_multiply():
    """Test the multiply function."""
    assert multiply(2, 3) == 6
    assert multiply(-1, 1) == -1
    assert multiply(0, 5) == 0

def test_divide():
    """Test the divide function."""
    assert divide(6, 3) == 2.0
    assert divide(-6, 3) == -2.0
    try:
        divide(5, 0)
    except ValueError as e:
        assert str(e) == "Cannot divide by zero."
    else:
        assert False, "Expected ValueError not raised"

# If using pytest, you can run the tests with the following command:
# pytest -v --tb=short tests/sample_test.py
# This will execute the tests defined in this file and report the results.
# To run the tests, you can simply call the test functions directly or use a test runner like pytest.


def test_bank_set_initial_amount(bank_account_with_balance):
    """Test the BankAccount class initial balance."""
    # account = BankAccount(100.0)
    assert bank_account_with_balance.get_balance() == 100.0

def test_bank_default_initial_amount(zero_bank_account):
    """Test the BankAccount class default initial balance."""
    print("Testing default initial amount of BankAccount using fixture")
    # account = BankAccount()
    assert zero_bank_account.get_balance() == 0.0

def test_withdraw(bank_account_with_balance):
    """Test the withdraw method of BankAccount."""
    # account = BankAccount(100.0)
    bank_account_with_balance.withdraw(50.0)
    assert bank_account_with_balance.get_balance() == 50.0
    with pytest.raises(InsufficientFundsError):
        bank_account_with_balance.withdraw(100.0)

def test_deposit(bank_account_with_balance):
    """Test the deposit method of BankAccount."""
    # account = BankAccount(100.0)
    bank_account_with_balance.deposit(50.0)
    assert bank_account_with_balance.get_balance() == 150.0
    try:
        bank_account_with_balance.deposit(-20.0)
    except ValueError as e:
        assert str(e) == "Cannot deposit a negative amount."
    else:
        assert False, "Expected ValueError not raised"

def test_collect_interest(bank_account_with_balance):
    """Test the collect_interest method of BankAccount."""
    # account = BankAccount(100.0)
    bank_account_with_balance.collect_interest(10)  # 10% interest
    assert bank_account_with_balance.get_balance() == 110.0
    try:
        bank_account_with_balance.collect_interest(-5)  # Negative interest rate
    except ValueError as e:
        assert str(e) == "Interest rate cannot be negative."
    else:
        assert False, "Expected ValueError not raised"


@pytest.mark.parametrize(
    "deposit_amount, withdraw_amount, expected_balance",
    [
        (100.0, 30.0, 70.0),
        (200.0, 50.0, 150.0),
        (300.0, 100.0, 200.0),
        (50.0, 20.0, 30.0),
        (0.0, 0.0, 0.0),
        (1000.0, 500.0, 500.0),
    ])
def test_bank_transactions(zero_bank_account, deposit_amount, withdraw_amount, expected_balance):
    """Test a series of bank transactions."""
    print("Testing a series of bank transactions")
    # account = BankAccount(0.0)
    zero_bank_account.deposit(deposit_amount)
    zero_bank_account.withdraw(withdraw_amount)
    assert zero_bank_account.get_balance() == expected_balance


def test_insufficient_funds(bank_account_with_balance):
    """Test insufficient funds during withdrawal."""
    print("Testing insufficient funds during withdrawal")
    # account = BankAccount(100.0)
    # Attempt to withdraw more than the balance
    print("Attempting to withdraw more than the balance")
    with pytest.raises(InsufficientFundsError):
        bank_account_with_balance.withdraw(200.0)


def test_negative_deposit(zero_bank_account):
    """Test negative deposit."""
    print("Testing negative deposit")
    # account = BankAccount(0.0)
    try:
        zero_bank_account.deposit(-50.0)  # Attempt to deposit a negative amount
    except ValueError as e:
        assert str(e) == "Cannot deposit a negative amount."
    else:
        assert False, "Expected ValueError not raised"

def test_negative_interest(bank_account_with_balance):
    """Test negative interest rate."""
    print("Testing negative interest rate")
    # account = BankAccount(100.0)
    try:
        bank_account_with_balance.collect_interest(-5)  # Attempt to collect negative interest
    except ValueError as e:
        assert str(e) == "Interest rate cannot be negative."
    else:
        assert False, "Expected ValueError not raised"
