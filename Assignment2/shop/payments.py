"""Payment methods.

All payment methods play the same role — "take this amount from the
customer" — so they share the PaymentMethod interface. How they do it
differs: a card adds a processing fee and checks the credit limit, cash
checks the amount handed over and gives change.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import count
from typing import Optional


@dataclass
class PaymentResult:
    success: bool
    method: str
    amount_due: float
    amount_charged: float
    message: str
    reference: Optional[str] = None


class PaymentMethod(ABC):
    _next_ref = count(1)

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable description of the method."""

    @abstractmethod
    def pay(self, amount: float) -> PaymentResult:
        """Attempt to collect `amount` and report what happened."""

    def _new_reference(self, prefix: str) -> str:
        return f"{prefix}-{next(PaymentMethod._next_ref):05d}"


class CardPayment(PaymentMethod):
    PROCESSING_FEE_RATE = 0.02

    def __init__(self, holder: str, card_number: str, available_credit: float):
        digits = card_number.replace(" ", "")
        if not digits.isdigit() or not 13 <= len(digits) <= 19:
            raise ValueError("Invalid card number.")
        self.holder = holder
        self._last4 = digits[-4:]            # the full number is never stored
        self.available_credit = available_credit

    @property
    def name(self) -> str:
        return f"Card ****{self._last4}"

    def pay(self, amount: float) -> PaymentResult:
        fee = round(amount * self.PROCESSING_FEE_RATE, 2)
        charge = round(amount + fee, 2)
        if charge > self.available_credit:
            return PaymentResult(
                False, self.name, amount, 0.0,
                f"Declined: needs ${charge:.2f}, only ${self.available_credit:.2f} available.",
            )
        self.available_credit = round(self.available_credit - charge, 2)
        return PaymentResult(
            True, self.name, amount, charge,
            f"Approved for {self.holder}. Includes 2% card fee of ${fee:.2f}.",
            self._new_reference("CARD"),
        )


class CashPayment(PaymentMethod):
    def __init__(self, amount_tendered: float):
        self.amount_tendered = amount_tendered

    @property
    def name(self) -> str:
        return "Cash"

    def pay(self, amount: float) -> PaymentResult:
        if self.amount_tendered < amount:
            short = round(amount - self.amount_tendered, 2)
            return PaymentResult(
                False, self.name, amount, 0.0,
                f"Insufficient cash: ${self.amount_tendered:.2f} tendered, ${short:.2f} short.",
            )
        change = round(self.amount_tendered - amount, 2)
        return PaymentResult(
            True, self.name, amount, amount,
            f"Tendered ${self.amount_tendered:.2f}, change given ${change:.2f}.",
            self._new_reference("CASH"),
        )
