import xml.etree.ElementTree as ET

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
    tree = ET.parse('input_data.xml')
    root = tree.getroot()
except FileNotFoundError:
    print("Файл не найден.")
except ET.ParseError:
    print("Ошибка при чтении данных из файла. Проверьте формат XML.")
else:
    products = []
    for product_element in root.findall('./products/product'):
        product_id = int(product_element.attrib['id'])
        name = product_element.find('name').text
        description = product_element.find('description').text
        price = float(product_element.find('price').text)
        stock_quantity = int(product_element.find('stock_quantity').text)
        discount_percentage = float(product_element.find('discount_percentage').text)  

        discount_attr = product_element.attrib.get('discount_percentage')
        if discount_attr:
            discount_percentage = float(discount_attr)
            price = price * (100 - discount_percentage) / 100  # Применить скидку к цене
        if discount_percentage > 0:
            product = DiscountedProduct(product_id, name, description, price, stock_quantity, discount_percentage)
        else:
            product = Product(product_id, name, description, price, stock_quantity)
        products.append(product)

    customers = []
    customer_element = root.find('./customers/customer')
    customer_id = int(customer_element.find('customer_id').text)
    name = customer_element.find('name').text
    email = customer_element.find('email').text
    customer = Customer(customer_id, name, email)
    customers.append(customer)

    cart = ShoppingCart()

    for product in products:
        cart.add_product(product)

    total = cart.calculate_total()

    output_root = ET.Element("purchase")

    products_element = ET.SubElement(output_root, "products")
    for product in products:
        product_element = ET.SubElement(products_element, "product", id=str(product.product_id))
        ET.SubElement(product_element, "name").text = product.name
        ET.SubElement(product_element, "price").text = str(product.price)

    customer_element = ET.SubElement(output_root, "customer")
    ET.SubElement(customer_element, "customer_id").text = str(customers[0].customer_id)
    ET.SubElement(customer_element, "name").text = customers[0].name
    ET.SubElement(customer_element, "email").text = customers[0].email

    ET.SubElement(output_root, "total").text = str(total)

    output_tree = ET.ElementTree(output_root)
    output_tree.write("purchase_data.xml")

    print("Данные о покупке успешно записаны в purchase_data.xml")
