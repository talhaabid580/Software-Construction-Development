"""Demonstration of the Online Shopping and Payment Processing System."""
from shop.checkout import Checkout
from shop.order import Customer, Order
from shop.payments import CardPayment, CashPayment, PaymentResult
from shop.products import DigitalProduct, PhysicalProduct

LINE = "-" * 64


def banner(title: str) -> None:
    print("=" * 64)
    print(title)
    print("=" * 64)


def print_order(order: Order) -> None:
    print(f"Order #{order.order_id} for {order.customer.name}  [{order.status}]")
    print(LINE)
    for item in order.items:
        p = item.product
        print(f"{item.quantity} x {p.name:<34} ${item.base_cost():>8.2f}")
        print(f"    + {p.extra_cost_label():<32} ${item.extra_cost():>8.2f}")
        print(f"    ({p.delivery_info()})")
    print(LINE)
    print(f"{'Subtotal':<38} ${order.subtotal():>8.2f}")
    print(f"{'Shipping / digital tax':<38} ${order.extra_charges():>8.2f}")
    print(f"{'ORDER TOTAL':<38} ${order.total():>8.2f}")


def print_result(result: PaymentResult, order: Order) -> None:
    outcome = "SUCCESS" if result.success else "FAILED"
    print(f"\nPayment via {result.method}: {outcome}")
    print(f"  {result.message}")
    if result.success:
        print(f"  Amount charged: ${result.amount_charged:.2f}   Ref: {result.reference}")
    print(f"  Order status is now {order.status}")


def checkout(order: Order, method) -> None:
    print_result(Checkout(order, method).process(), order)


def main() -> None:
    # --- Catalogue -------------------------------------------------------
    keyboard = PhysicalProduct("PHY-001", "Mechanical Keyboard", 79.99, weight_kg=1.2)
    book = PhysicalProduct("PHY-002", "Python Crash Course (paperback)", 35.50, weight_kg=0.9)
    ebook = DigitalProduct("DIG-001", "Clean Code (e-book)", 24.99, "EPUB download")
    course = DigitalProduct("DIG-002", "Online Course: OOP in Python", 49.00, "Streaming access")

    ayesha = Customer("Ayesha Khan", "ayesha@example.com", "12 Clifton Rd, Karachi")
    bilal = Customer("Bilal Ahmed", "bilal@example.com", "45 Gulshan Ave, Karachi")

    # --- Scenario 1: mixed order paid by card ----------------------------
    banner("SCENARIO 1: Mixed physical + digital order, paid by card")
    order1 = Order(ayesha)
    order1.add_product(keyboard)
    order1.add_product(ebook)
    order1.add_product(course)
    print_order(order1)
    checkout(order1, CardPayment("Ayesha Khan", "4111 1111 1111 1111", available_credit=500))

    # --- Scenario 2: physical order paid in cash -------------------------
    print()
    banner("SCENARIO 2: Physical order, paid in cash")
    order2 = Order(bilal)
    order2.add_product(book, 2)
    order2.add_product(keyboard)
    print_order(order2)
    checkout(order2, CashPayment(amount_tendered=170.00))

    # --- Scenario 3: declined card, then same order paid in cash ---------
    print()
    banner("SCENARIO 3: Card declined, customer switches to cash")
    order3 = Order(bilal)
    order3.add_product(course)
    order3.add_product(book)
    order3.add_product(ebook, 2)   # two licences
    print_order(order3)
    checkout(order3, CardPayment("Bilal Ahmed", "5500 0000 0000 0004", available_credit=100))
    checkout(order3, CashPayment(amount_tendered=150.00))


if __name__ == "__main__":
    main()
