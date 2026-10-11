
class ShoppingCart:
    def __init__(self):
        
        self.items = []

    def add_item(self, product_name, price, quantity):

        item = {
            "name": product_name,
            "price": price,
            "quantity": quantity
        }

        self.items.append(item)

    def calculate_total(self):

        total = 0

        for item in self.items:
            total += item["price"] * item["quantity"]

        return total


cart1 = ShoppingCart()
cart2 = ShoppingCart()

cart1.add_item("Keyboard", 2500, 1)
cart1.add_item("Mouse", 1200, 2)

cart2.add_item("Headphones", 3500, 1)
cart2.add_item("USB Cable", 500, 3)

print("Cart 1 Items:", cart1.items)
print("Cart 1 Total:", cart1.calculate_total())

print()

print("Cart 2 Items:", cart2.items)
print("Cart 2 Total:", cart2.calculate_total())
