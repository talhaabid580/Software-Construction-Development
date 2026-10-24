"""Checkout: brings an order and a payment method together."""
from shop.order import Order
from shop.payments import PaymentMethod, PaymentResult


class Checkout:
    def __init__(self, order: Order, payment_method: PaymentMethod):
        self.order = order
        self.payment_method = payment_method

    def process(self) -> PaymentResult:
        if self.order.is_empty():
            raise ValueError("Cannot check out an empty order.")
        if self.order.status == Order.PAID:
            raise RuntimeError(f"Order #{self.order.order_id} is already paid.")

        amount = self.order.total()
        # Polymorphic call: Checkout does not know or care which method this is.
        result = self.payment_method.pay(amount)
        if result.success:
            self.order.mark_paid()
        return result
