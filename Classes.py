# домашнє завдання Давидченко
# pull request_1
import math

class ProductError(Exception):
    
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'Error with class Product_some {0}'.format(self.message)
        else:
            return 'Error with class Product_some has been raised'


class Product:
    def __init__(self, name, price):
        """
        конструктор класу Product
        :param name: найменування продукту
        :param price: вартість одиниці продукти
        """

        if name == '':
            raise ProductError('error in __init__, invalid name of Product')
        else:
            self.name = name
        if price > 0:
            self.price = price
        else:
            raise ProductError('error in __init__, invalid price  value')

    def total_price(self, quantity):
        """
        метод повертає вартість продукту у кількості quantity
        :param quantity: кількість продукту
        :return: вартість вказаної кількості продукту
        """
        return round(self.price * quantity, 2)


class ProductSome(Product):
    """
    клас - продукт певної кількості
    має атрибут quantity, який визначає кількість товару 
    """

    def __init__(self, product_i, quantity=0):
        """
        метод визначає поведінку при ініціалізації об'єкту. Зокрема, коли quantity < 0, то 
        quantity встановлюється = 0. Така поведінка потрібна для визначення операцій з продуктами в корзині.

        :param product_i: екземпляр класу Product
        :param quantity: кількість продукту
        """
        Product.__init__(self, product_i.name, product_i.price)
        if quantity > 0:
            self.quantity = quantity
        else:
            self.quantity = 0

    def inc(self, quantity):
        """
        метод збільшує кількість продукту на значення quantity
        :param quantity: 
        :return: нічого не повертає
        """
        self.quantity += quantity

    def dec(self, quantity):
        """
        метод зменьшує кількість продукту на значення quantity.
        Здійснюється контроль за тим, що б self.quantity не було меньше нуля

        :param quantity:
        :return:
        """
        if self.quantity < quantity:
            result = self.quantity
            self.quantity = 0
        else:
            result = quantity
            self.quantity -= quantity
        return result

    def __add__(self, other):
        """
        перевизначення операції + для екземплярів класу ProductSome.
        метод здійснюєтья додавання кількості продукту, створує новий екземпляр класу з новим значенням
        кількості продукту.
        У методі також  здійснюється контроль за типами операндів

        :param other: має бути одного типу з self
        :return: ProductSome з новим значенням кількості продукту
        """

        if type(self) == type(other) and self.name == other.name:

            return ProductSome(self, self.quantity + other.quantity)
        else:
            raise ProductError('error in __add__, type mismatch')

    def __sub__(self, other):
        """
        перевизначення операції -  для екземплярів класу ProductSome.
        метод здійснюється додавання кількості продукту, створює новий екземпляр класу з новим значенням
        кількості продукту.
        У методі також  здійснюється контроль за типами операндів.
        При створенні екземпляру продукту

        :param other:
        :return:
        """

        if type(self) == type(other) and self.name == other.name:

            return ProductSome(self, self.quantity - other.quantity)
        else:
            raise ProductError('error in __add__, type mismatch')

    def __str__(self):
        """
        метод здійснює перетворення об'єкту у строку
        :return: повертає об'єкт у строковому вигляді
        """
        return 'name {0}, price {1}, quantity {2}'.format(self.name, self.price, self.quantity)



class ShoppingCart:
    """
    клас "Корзина з товарами"
    """
    def __init__(self):
        # словник ключ - назван продукту, значення екземпляр  класу  ProductSome
        self.products = {}
        # вартість корзини
        self.__total_price__ = 0

    def __str__(self):
        """
        строкове відображення корзини
        :return: повертає строку - строкове відображення корзини
        """
        str_res = 'ShoppingCart \n'
        for key in self.products.keys():
            str_res += '\'{0}\' {1} * {2} = {3} \n'.format(key, self.products[key].quantity, self.products[key].price,
                                                           round(self.products[key].quantity * self.products[key].price,
                                                                 2))
        str_res += '-' * 20 + '\n'
        str_res += 'total {0} \n'.format(self.__total_price__)

        return str_res

    def add (self, product_inst: Product, quantity):
        """
            метод додає товар певної кількості до корзини
            :param product_inst: екземпляр класу Product - продукт, що додається
            :param quantity: кількість продукту що додається
            :return: нічого не повертає
        """

        self.products.setdefault(product_inst.name, ProductSome(product_inst))
        self.products[product_inst.name].inc(quantity)
        self.__total_price__ += round(quantity * product_inst.price, 2)


    def rm(self, product_inst: Product, quantity=0):
        """
        метож видаляє з корзину товар product_inst у кількості quantity.
        Якщо quantity не вказано або == 0 то видаляєтья позиція повність
        :param product_inst: ексземпляр класу Product
        :param quantity: кількість на яку потрібно зменьшити товар у корзині
        :return:
        """

        if self.products.get(product_inst.name):
            dec = self.products[product_inst.name].dec(quantity)
            self.__total_price__ -= round(dec * product_inst.price, 2)
            if self.products[product_inst.name].quantity == 0:
                self.products.pop(product_inst.name)
        else:
            raise ProductError('error in ShoppingCart.rm , товар {0} відсутній у корзині'.format (product_inst.name))


    def sum(self):
        """
        метод підраховує вартість корзини
        :return:
        """
        sum_res = 0
        for key in self.products.keys():
            sum_res += round(self.products[key].quantity * self.products[key].price, 2)
        print('total {0} '.format(sum_res))
        # перевіряємо чи зійшлось підрахована вартість корзини із значченням вартості, що зберігається в атрібуті
        # __total_price__
        if not math.isclose(sum, self.__total_price__):
            raise ProductError('error in ShoppingCart.sum вартість корзини не вірно визначена')


    def get_price(self):
        """
        метод повертає вартість корзини
        :return:
        """
        return self.__total_price__


if __name__ == '__main__':
    cart = ShoppingCart()

    tomato = Product('tomato', 34.50)
    mango = Product('mango', 60.50)
    tomato1 = ProductSome(tomato, 3)
    tomato2 = ProductSome(tomato, 0.5)
    beef = Product('beef', 168.75)

    cart.add(tomato, 2)
    cart.add(beef, 1.5)
    cart.add(tomato, 0.5)
    print(cart)

    cart.rm(tomato, 2.5)
    #cart.rm(mango, 2.5)

    print(cart)
    cart.sum()

    print((tomato1 + tomato2))
    # (tomato1 + beef).print()
    print(tomato2 - tomato1)
