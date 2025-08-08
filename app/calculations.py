
def add(num1: int, num2: int) -> int:
    """Add two numbers."""
    return num1 + num2

def subtract(num1: int, num2: int) -> int:
    """Subtract two numbers."""
    return num1 - num2

def multiply(num1: int, num2: int) -> int:
    """Multiply two numbers."""
    return num1 * num2

def divide(num1: int, num2: int) -> float:
    """Divide two numbers."""
    if num2 == 0:
        raise ValueError("Cannot divide by zero.")
    return num1 / num2

class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds in a bank account."""
    pass

class BankAccount:
    """A simple bank account class."""
    
    def __init__(self, balance: float = 0.0):
        self.balance = balance

    def deposit(self, amount: float) -> None:
        """Deposit money into the account."""
        if amount < 0:
            raise ValueError("Cannot deposit a negative amount.")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraw money from the account."""
        if amount < 0:
            raise ValueError("Cannot withdraw a negative amount.")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds.")
        self.balance -= amount
    
    def collect_interest(self, rate: float) -> None:
        """Collect interest on the current balance."""
        if rate < 0:
            raise ValueError("Interest rate cannot be negative.")
        interest = self.balance * (rate / 100)
        self.balance += interest

    def get_balance(self) -> float:
        """Get the current balance."""
        return self.balance
    
