class Product:
    def __init__(self, name, price, category, discount, stock=1):
        """
        Класс товара

        Args:
            name (str): Имя товара
            price (float): Цена товара
            category (str): Категория товара
            discount (float): Скидка (в процентах)
            stock (int, optional): Количество оставшихся единиц товара
        """
        self.name = name
        self.price = price * (1 - discount / 100) 
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
        """
        Пишет инфу
        """
        return f"Товар {self.name} стоит {self.price} денег, относится к категории {self.category}, а на складе сейчас {self.stock} штук"
    
    def get_price(self):
        """
        Возвращает цену
        """
        return round(self.price, 2)

    def __str__(self):
        """
        Позволяет запринтить инфу человекочитаемым образом
        """
        return self.info()
    

class ShoppingCart:
    def __init__(self):
        """
        Класс корзины
        """
        self.cart = dict()
    def add_product(self, product):
        """
        Добавляет товар в корзину

        Args:
            product (Product): Товар
        """
        if product.stock == 0:
            print("Товара нет в продаже!")
        else:
            product.stock -= 1
            if not product in self.cart:
                self.cart[product] = product.price
            else:
                self.cart[product] += product.price

    def remove_product(self, product):
        """
        Удаляет товар из корзины

        Args:
            product (Product): Товар
        """
        if not product in self.cart:
            print("Такого продукта в корзине нет!")
        else:
            product.stock += 1
            self.cart[product] -= product.price
            if self.cart[product] == 0:
                self.cart.pop(product)

    def info(self):
        """
        Выдаёт человекочитаемый словарь
        
        Returns:
            self.readable_dict (dict): человекочитаемый словарь
        """
        self.readable_dict = dict()
        for key in self.cart.keys():
            self.readable_dict[key.name] = self.cart[key]
        return f"{self.readable_dict}"

    def __str__(self):
        """
        Позволяет запринтить инфу по людски
        """
        return self.info()
    
class Order:
    def __init__(self, shopping, customer, tax):
        """
        Класс конкретного заказа

        Args:
            shopping (ShoppingCart): корзина
            customer (Customer): покупатель
            tax (float): налог
        """
        self.shopping = shopping
        self.tax = tax
        self.customer = customer
        self.cart_price = 0

    def payment(self):
        """
        Просчёт суммы заказа, добавление заказа в историю заказов
        """
        for product in self.shopping.cart:
            self.cart_price += self.shopping.cart[product]  * (1 + self.tax / 100)
        if self.customer.money >= self.cart_price:
            self.customer.money -= self.cart_price
            self.customer.shopping_history.append(f"{', '.join(self.shopping.readable_dict.keys())} на сумму {round(self.cart_price, 2)}")
            return f"Вы заплатили {self.cart_price:.2f}"
        else:
            return f"Денег недостаточно!"

class Customer:
    def __init__(self, name, money):
        """
        Класс покупателя
        
        Args:
            name (str): имя
            money (str): количество денег
        """
        self.money = money
        self.shopping_history = []
        self.name = name
    def info(self):
        """
        Возвращает историю покупок
        """
        return self.shopping_history
