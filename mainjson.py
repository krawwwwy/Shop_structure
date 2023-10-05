import json

class Product:
    def __init__(self, product_id, name, description, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity

    def display_info(self):
        print(f"Product ID: {self.product_id}")
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"Price: ${self.price}")
        print(f"Stock Quantity: {self.stock_quantity}")
        print("------------------------------")

class DiscountedProduct(Product):
    def __init__(self, product_id, name, description, price, stock_quantity, discount_percentage):
        # Вызываем конструктор базового класса Product
        super().__init__(product_id, name, description, price, stock_quantity)
        self.discount_percentage = discount_percentage
        self.preprice = self.price
        self.price = self.price * (100 - discount_percentage) / 100
    # Переопределяем метод для отображения информации о продукте с учетом скидки
    def display_info(self):
        print(f"Product ID: {self.product_id}")
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"Price: ${self.price} (Discounted from ${self.preprice})")
        print(f"Stock Quantity: {self.stock_quantity}")
        print("------------------------------")

class ShoppingCart:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        if product.stock_quantity != 0:
            self.products.append(product)
        else:
            raise ValidationError("Product out of stock")

    def remove_product(self, product):
        if len(products):
            self.products.remove(product)
        else:
            raise ValidationError("There are no products in the cart")

    def calculate_total(self):
        total = 0
        for product in self.products:
            total += product.price
        return total

    def checkout(self):
        total = self.calculate_total()
        print(f"Total: ${total}")
        print("Thank you for your purchase!")


class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def display_info(self):
        print(f"Customer ID: {self.customer_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print("------------------------------")

class ValidationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

try:
    with open('input_data.json', 'r') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print("Файл не найден.")
except json.JSONDecodeError:
    print("Ошибка при чтении данных из файла. Проверьте формат данных.")
else:
    products = []
    for product_data in data['products']:
        if "discount_percentage" in product_data:
            product = DiscountedProduct(product_data["id"], product_data["name"], product_data["description"],
                                        product_data["price"], product_data["stock_quantity"],
                                        product_data["discount_percentage"])
        else:
            product = Product(product_data["id"], product_data["name"], product_data["description"],
                              product_data["price"], product_data["stock_quantity"])
        products.append(product)

    customers = []
    for customer_data in data["customers"]:
        customer = Customer(customer_data["customer_id"], customer_data["name"], customer_data["email"])
        customers.append(customer)

    cart = ShoppingCart()

    for product in products:
        cart.add_product(product)

    total = cart.calculate_total()

    purchase_data = {
        "products": [{"name": product.name, "price": product.price} for product in products],
        "customer": {"name": customers[0].name, "email": customers[0].email},
        "total": total
    }


    with open('purchase_data.json', 'w') as json_output_file:
        json.dump(purchase_data, json_output_file, indent=4)

    print("Данные о покупке успешно записаны в purchase_data.json")
