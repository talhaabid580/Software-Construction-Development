"""Customer, order lines and orders.

An Order is composed of OrderItems that it creates and owns; each OrderItem
refers to a Product from the catalogue and records how many were ordered.
The Order never needs to know which kind of product it holds — it simply
asks every item for its costs.
"""
from dataclasses import dataclass
from itertools import count

from shop.products import Product


@dataclass
class Customer:
    name: str
    email: str
    address: str


class OrderItem:
    """One line of an order: a product and a quantity."""

    def __init__(self, product: Product, quantity: int):
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        self.product = product
        self.quantity = quantity

    def base_cost(self) -> float:
        return self.product.base_cost(self.quantity)

    def extra_cost(self) -> float:
        # Polymorphic call: shipping for physical items, tax for digital ones.
        return self.product.extra_cost(self.quantity)

    def total(self) -> float:
        return self.base_cost() + self.extra_cost()


class Order:
    PENDING = "PENDING"
    PAID = "PAID"

    _next_id = count(1001)

    def __init__(self, customer: Customer):
        self.order_id = next(Order._next_id)
        self.customer = customer
        self.status = Order.PENDING
        self._items: list[OrderItem] = []

    def add_product(self, product: Product, quantity: int = 1) -> None:
        if self.status != Order.PENDING:
            raise RuntimeError("Cannot change an order that has already been paid.")
        for item in self._items:
            if item.product is product:          # same product again: merge lines
                item.quantity += quantity
                return
        self._items.append(OrderItem(product, quantity))

    @property
    def items(self) -> tuple[OrderItem, ...]:
        return tuple(self._items)               # read-only view for callers

    def is_empty(self) -> bool:
        return not self._items

    def subtotal(self) -> float:
        return round(sum(item.base_cost() for item in self._items), 2)

    def extra_charges(self) -> float:
        return round(sum(item.extra_cost() for item in self._items), 2)

    def total(self) -> float:
        return round(self.subtotal() + self.extra_charges(), 2)

    def mark_paid(self) -> None:
        self.status = Order.PAID
