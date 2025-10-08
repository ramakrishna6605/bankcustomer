class Bank_Account:
    _owner: str
    _balance: float
    _active: bool = True
    _cheque_book_requested: bool = False

class SavingsAccount(BankAccount):
    def __init__(self, name: str, initial_balance: float, pin: str, daily_withdraw_limit: float = 1000.0):
        self.__pin = pin  # private
        self.__atm_card_requested = False  # private
        super().__init__(_owner=name, _balance=initial_balance)
        self._daily_withdraw_limit = daily_withdraw_limit
        self._withdrawn_today = 0.0

    def __verify_pin(self, pin):
        if pin != self.__pin:
            raise PINError("Incorrect PIN.")

    def check_balance(self, pin: str):
        self.__verify_pin(pin)
        return super().check_balance()

    def withdraw(self, amount: float, pin: str):
        self.__verify_pin(pin)
        if not self._active:
            raise InactiveAccountError("Account is inactive/frozen.")
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be greater than zero.")
        if amount > self._balance:
            raise InsufficientFundsError("Insufficient funds.")
        if (self._withdrawn_today + amount) > self._daily_withdraw_limit:
            raise InsufficientFundsError("Amount exceeds daily withdrawal limit.")
        self._balance -= amount
        self._withdrawn_today += amount
        return self._balance

    def deposit(self, amount: float, pin: str):
        self.__verify_pin(pin)
        return super().deposit(amount)

    def request_atm_card(self):
        if self.__atm_card_requested:
            raise AlreadyRequestedError("ATM card already requested.")
        self.__atm_card_requested = True
        return "ATM card request approved."

    def request_cheque_book(self):
        return super().request_cheque_book()

    def freeze_account(self):
        if not self._active:
            raise AlreadyRequestedError("Account already frozen.")
        self._freeze()
        return "Account frozen."

    def unfreeze_account(self):
        if self._active:
            raise AlreadyRequestedError("Account already active.")
        self._unfreeze()
        self._withdrawn_today = 0.0
        return "Account unfrozen."

    @property
    def _get_protected_balance(self):
        return self._balance


class BusinessAccount(BankAccount):
    def __init__(self, business_name: str, initial_balance: float, overdraft_limit: float = 5000.0, loan_limit: float = 20000.0):
        super().__init__(_owner=business_name, _balance=initial_balance)
        self._overdraft_limit = overdraft_limit
        self._loan_limit = loan_limit
        self._loan_approved = 0.0

    def withdraw(self, amount: float):
        if not self._active:
            raise InactiveAccountError("Account is inactive/frozen.")
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be greater than zero.")
        if amount > (self._balance + self._overdraft_limit):
            raise InsufficientFundsError("Amount exceeds balance + overdraft limit.")
        self._balance -= amount
        return self._balance

    def request_loan(self, amount: float):
        if amount <= 0:
            raise InvalidAmountError("Loan amount must be greater than zero.")
        if amount > self._loan_limit:
            raise InsufficientFundsError("Requested loan exceeds loan limit.")
        self._loan_approved += amount
        return f"Loan for {amount} approved."

    def request_cheque_book(self):
        return super().request_cheque_book()