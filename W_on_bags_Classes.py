from typing import Union
import logging

def debug_func(func):
    """
    декоратор для logger
    :param func:
    :return:
    """

    def wrapper(*args):
        logger.debug('виклик функції {0}'.format(func.__name__))
        for arg in args:

            logger.debug(' функції передані аргументи %s', arg)
        logger.debug('результат виконання функції {0}  = {1}'.format(func.__name__, func(*args)))

    return wrapper

class ProductError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Product:
    def __init__(self, name: str, price: float) -> None:
        """
        конструктор класу Product
        :param name: найменування продукту
        :param price: вартість одиниці продукти
        """
        self.name = name
        self.price = price

    def validate(self) -> bool:
        """
        метод здійснює валідацію значень екземпляру класа
        :return:
        """
        return  self.name and self.price > 0

    def total_price(self, quantity: float) -> float:
        """
        метод повертає вартість продукту у кількості quantity
        :param quantity: кількість продукту
        :return: вартість вказаної кількості продукту
        """
        if self.validate():
            return round(self.price * quantity, 2)
        else:
            raise ProductError('none validate object, product name {0}'.format(self.name))

    def __eq__(self, other) -> bool:
        if isinstance(other, Product):
            return self.name == other.name and self.price == other.price
        else:
            return False

    # def __ne__(self, other) -> bool:
    #     return not self.__eq__(other)

    def total_price_str(self, quantity) -> str:
        """
        метод повертає строку-формулу розрахунку вартості
        :param quantity:
        :return: str - формулf розрахунку вартості
        """
        return f'\'{self.name}\' {quantity} * {self.price} = {self.total_price(quantity)}'


class ShoppingCart:
    """
    клас "Корзина з товарами"
    """

    #@debug_func
    def __init__(self):

        self.products: list[Product] = []
        self.quantity: list[Union[int, float]] = []

    def is_empty(self) -> bool:
        """
        для майбутнього використання
        :return:
        """
        return not self.products

    def get_num_goods(self) -> int:
        """
        для майбутнього використання
        :return:
        """
        return len(self.products)

    # def get_product_index(self, product: Product) -> int:
    #     """
    #     метод повертає індекс продукту Product в корзині.
    #     якщо продукту в корзині немає, то повертається -1
    #     :param product: екземпляр класу Product
    #     :return: індекс продукту
    #     """
    #     try:
    #         return self.products.index(product)
    #     except ValueError:
    #         raise ProductError(f'продукту немає у списку, product name {product}')

    def get_quantity(self, product: Product) -> Union[int, float]:
        """
        метод повертає кількість продукту product у корзині
        якщо такого продукту у корзині немає, то повертається нуль
        :param product: екземпляр класу  Product
        :return: кількість продукту Union[int, float]
        """
        try:
            return self.quantity[self.products.index(product)]
        except ValueError:
            raise ProductError(f'продукту немає у списку, product name {product}')


    #@debug_func
    def add(self, product_inst: Product, quantity) -> None:
        """
        метод додає продукт у кошик
        :param product_inst: екз класу Product
        :param quantity: кількість продукту
        :return:
        """

        if product_inst not in self.products:
            self.products.append(product_inst)
            self.quantity.append(quantity)
        else:
            self.quantity[self.products.index(product_inst)] += quantity

        idx = self.products.index(product_inst)
        if self.quantity[idx] <= 0:
            self.pop(product_inst)

    def pop(self, product: Product) -> None:
        """
        видаляє із списків self.products та self.quantity
        елементи з індексом index
        :param index: індекс елементу
        :return: None
        """
        i = self.products.index(product)
        self.products.pop(i)
        self.quantity.pop(i)

    def sub(self, product_inst: Product, quantity=0) -> None:
        """
        зменьшує кількість товару Product у корзина на кількість quantity
        Якщо quantity = 0, то видаляеться увест товар Product із корзини
        Якщо кількість товару, що в результаті зменьшення = 0, то товар видаляеться із корзини
        :param product_inst:
        :param quantity:
        :return:
        """
        quantity = - abs(quantity)
        return self.add(product_inst, quantity)


    def total_price(self) -> float:
        """
        обраховуеться вартість корзини
        :return: вартість корзини
        """
        total = 0
        for product, quantity in zip(self.products, self.quantity):
            total += product.total_price(quantity)

        return round(total, 2)

    def __str__(self):
        """
        строкове відображення корзини
        :return: повертає строку - строкове відображення корзини
        """
        res_str = ['']
        res_str.append('ShoppingCart')
        for product, quantity in zip(self.products, self.quantity):
            res_str.append(product.total_price_str(quantity))
        res_str.append('-' * 20)
        res_str.append('total {0}'.format(self.total_price()))
        res_str = '\n'.join(res_str)

        return res_str


# і тут замовник каже: зроби функціонал з дісконтом

class ProductDiscont(Product):

    def __init__(self, name: str, price: Union[int, float], discont: Union[int, float],
                 rules: Union[int, float]) -> None:
        """

        :param name: найменування продукту, унікальне
        :param price: вартість одиниці продукту
        :param discont: знижка у відсотках
        :param rules: правила застосування знижки, кількість одиниць товару, з якої починається дісконт
        """
        super().__init__(name, price)
        self.disont = discont
        self.rules = rules

    def discont_count(self, quantity: Union[int, float]) -> Union[int, float]:
        """
        метод обраховує розмір знижки
        :param quantity: кількість товару
        :return: розмір знижки
        """
        if quantity > self.rules:
            discont = round(self.price / 100 * self.disont, 2)
        else:
            discont = 0
        return discont

    def total_price(self, quantity: Union[int, float]) -> Union[int, float]:
        return round(super().total_price(quantity) - self.discont_count(quantity),2)

    def total_price_str(self, quantity) -> str:

        res_str = []
        res_str.append(f'\'{self.name}\' {quantity} * {self.price} = {super().total_price(quantity)}')
        # якщо дісконт більше нуля, то відображаемо його у "квитанції"
        if self.discont_count(quantity) > 0:
            res_str.append(f'discont -{self.discont_count(quantity)}'.rjust(len(res_str[0]), " "))
            res_str.append(f'total {self.total_price(quantity):>}'.rjust(len(res_str[0]), " "))
        return '\n'.join(res_str)


if __name__ == '__main__':
    # ini logger instance
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG,
                        format="%(asctime)s - [%(levelname)s] -  %(name)s - \
    (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
                        datefmt='%d.%m.%y %I:%M:%S %p')

    logger.debug('start sript')
    tomato = Product('tomato', 34.50)
    tomato1 = Product('tomato', 34.51)
    mango = Product('mango', 60.50)

    print(tomato.total_price(1))

    cart = ShoppingCart()
    cart.add(tomato, 5)
    cart.add(tomato, 2)

    print(cart)
    cart.add(mango, 3.6)
    print(cart)
    cart.sub(tomato, 0.5)
    print(cart)

    tomato_disc = ProductDiscont("milk", 14.5, discont=10, rules=8)
    cart.add(tomato_disc, 9)
    print(cart)
    print('кільксть продукту -', cart.get_quantity(tomato))
    print('кільксть продукту -', cart.get_quantity(tomato_disc))
    cart.sub(tomato, 0.5)
    print('кільксть продукту -', cart.get_quantity(tomato))
    print('кільксть продукту -', cart.get_quantity(tomato_disc))
    mango = Product(' ', 0)
    print(mango!=tomato)
    print(cart.is_empty())

