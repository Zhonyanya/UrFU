class Product:
    def __init__(self, name, price, category, stock=1):
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock
    @property
    def quantity(self):
        return self.stock
    
    @quantity.setter
    def quantity(self, value):
        self.stock = value
        if self.stock < 0:
            self.stock = 0

    def info(self):
        return f"Товар {self.name} стоит {self.price} денег, относится к категории {self.category}, а на складе сейчас {self.stock} штук"
    
    def get_price(self):
        return self.price

    def __str__(self):
        return self.info()
    
class Order:
    def __init__(self, product, quantity, discount=0, tax=13):
        self.product = product
        self.quantity = quantity
        self.discount = discount
        self.tax = tax
    def order_info(self):
        return f"Заказ содержит {self.quantity} {self.product.name}. На него скидка в {self.discount}%"
    def price(self):
        nalog = self.product.get_price() * self.tax / 100
        skidka = self.product.get_price() * self.discount / 100
        return self.product.get_price() + nalog - skidka
    def __str__(self):
        return self.order_info()
    
class ShoppingCart:
    def __init__(self, *products):
        self.products = products
        self.cart = dict()
        for tovar in self.products:
            if not tovar in self.cart:
                self.cart[tovar] = tovar.price
