"""Product hierarchy for the online store.

Every product has a SKU, a name and a unit price. What differs between
product types is the *extra* cost they add to an order and how they are
delivered, so those operations are declared abstract in Product and each
subclass supplies its own behaviour.
"""
from abc import ABC, abstractmethod


class Product(ABC):
    """Data and behaviour shared by everything the store sells."""

    def __init__(self, sku: str, name: str, price: float):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.sku = sku
        self.name = name
        self.price = price

    def base_cost(self, quantity: int) -> float:
        """Price before any type-specific charges (same rule for all products)."""
        return self.price * quantity

    @abstractmethod
    def extra_cost(self, quantity: int) -> float:
        """Type-specific charge added on top of the base cost."""

    @abstractmethod
    def extra_cost_label(self) -> str:
        """Short name for the extra charge, used on the order summary."""

    @abstractmethod
    def delivery_info(self) -> str:
        """How the customer receives this product."""

    def __str__(self) -> str:
        return f"{self.name} [{self.sku}] ${self.price:.2f}"


class PhysicalProduct(Product):
    """A tangible item that has to be shipped; shipping is charged by weight."""

    SHIPPING_RATE_PER_KG = 3.00

    def __init__(self, sku: str, name: str, price: float, weight_kg: float):
        super().__init__(sku, name, price)
        if weight_kg <= 0:
            raise ValueError("Weight must be positive.")
        self.weight_kg = weight_kg

    def extra_cost(self, quantity: int) -> float:
        return self.weight_kg * quantity * self.SHIPPING_RATE_PER_KG

    def extra_cost_label(self) -> str:
        return "shipping"

    def delivery_info(self) -> str:
        return f"Shipped to address ({self.weight_kg} kg each)"


class DigitalProduct(Product):
    """A downloadable or online item: no shipping, but a digital services tax."""

    DIGITAL_TAX_RATE = 0.05

    def __init__(self, sku: str, name: str, price: float, access_type: str):
        super().__init__(sku, name, price)
        self.access_type = access_type  # e.g. "EPUB download", "Streaming access"

    def extra_cost(self, quantity: int) -> float:
        return self.base_cost(quantity) * self.DIGITAL_TAX_RATE

    def extra_cost_label(self) -> str:
        return "digital tax"

    def delivery_info(self) -> str:
        return f"{self.access_type} link sent by email"
