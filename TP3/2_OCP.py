class Discount:
    def __init__(self, price):
        self.price = price

    def apply_discount(self):
        return self.price

class VIPDiscount(Discount):
    def apply_discount(self):
        return self.price * 0.8  # 20% discount

# Question 1: Add a new discount for first-time customer (10% discount)
class FirstTimeCustomerDiscount(Discount):
    def apply_discount(self):
        return self.price * 0.9  # 10% discount

# Question 2: Add main call to test the code
if __name__ == '__main__':
    price = 1000

    regular = Discount(price)
    vip = VIPDiscount(price)
    first_time = FirstTimeCustomerDiscount(price)

    print(f"Original Price: ${price}")
    print(f"Regular Customer Price: ${regular.apply_discount()}")
    print(f"VIP Customer Price: ${vip.apply_discount()}")
    print(f"First Time Customer Price: ${first_time.apply_discount()}")