# Exceptions
class InvoiceError(Exception):
    pass
class InvalidPaymentStateError(InvoiceError):
    pass
class InvalidInvoiceAmountError(InvoiceError):
    pass
class DuplicateInvoiceError(InvoiceError):
    pass
class InvalidInvoiceCodeError(InvoiceError):
    pass

def make_commission_manager(initial_rate):
    rate = initial_rate

    def calculate_commission(amount):
        return round(amount * rate, 2)

    def update_rate(new_rate):
        nonlocal rate
        if not 0 <= new_rate <= 1:
            raise ValueError("Commission rate must be between 0 and 1")
        rate = new_rate

    return calculate_commission, update_rate

commission_calculator, update_commission_rate = make_commission_manager(0.15)

class Invoice:
    def __init__(self, code, amount, commission=None, status="pending"):
        self.__code = code
        self.__amount = amount
        self.__commission = commission
        self.__status = status

    def get_code(self):
        return self.__code
    def get_amount(self):
        return self.__amount
    def get_commission(self):
        return self.__commission
    def get_status(self):
        return self.__status
    def set_status(self, status):
        self.__status = status
    def set_commission(self, commission):
        self.__commission = commission
