"""

Реалізація класів "Продукт" та "Кошик для продуктів", методів

"""

from CartAndProductsError import ProductError, ProductArithOperError
import logging
from typing import Union, List

# ini logger instance
logger = logging.getLogger(__name__)
# виділяємо шлях до директорії виконання модуля
path = __file__.split('/')[:-1]
path = "/".join(path)

# виділяємо ім'я модуля без шляху до нього
fname = __file__.split('/')[-1].replace('.py', '')
logging.basicConfig(filename=f'{path}/log/{fname}.log',
                    filemode='w',
                    level=logging.DEBUG,
                    format="%(asctime)s - [%(levelname)s] - %(message)s",
                    datefmt='%d.%m.%y %I:%M:%S %p')


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


class Product:
    """
    Class Product: реалізує сутність категорії "продукт".
    Володіє атрибутами:
        name: найменування продукту
        price: вартість одиниці продукти
    Сукупність атрибутів name та price є унікальною.
    Реалізовані методи дозволяють виконувати низку арифметичних операцій над
    екземплярами класу Product
    """

    def __init__(self, name: str, price: float) -> None:
        """
        конструктор класу Product
        :param name: найменування продукту
        :param price: вартість одиниці продукти
        """
        self.name = name
        self.price = price
        logger.info(f'create instance {self.__class__} -  {self.name}, {self.price}')

    def validate(self) -> bool:
        """
        Метод здійснює валідацію значень екземпляру класу
        :return: повертає True коли ім'я не пусте та price > 0
        """
        return self.name and self.price > 0

    def total_price(self, quantity: float) -> float:
        """
        Метод повертає вартість продукту у кількості quantity
        :param quantity: кількість продукту
        :return: вартість вказаної кількості продукту
        """
        if self.validate():
            return round(self.price * quantity, 2)
        else:
            msg = f'none validate object, product name {self.name}'
            logger.error(msg, exc_info=True)
            raise ProductError(msg)

    def __eq__(self, other) -> bool:
        """
        метод реалізує логічний оператор '=='
        :param other: екземпляр класу Product
        :return: результат порівняння True or False
        """
        if isinstance(other, Product):
            return self.name == other.name and self.price == other.price

        else:
            return False

    def total_price_str(self, quantity: Union[int, float]) -> str:
        """
        Метод повертає строку-формулу розрахунку вартості.
        Cтрока - формула використовується у строковому відображенні
        відповідної позиції змісту кошик (у тому числі із розрахунком вартості
        цієї позиції)
        :param quantity: кількість продукту
        :return: str - формули розрахунку вартості
        """
        return f'\'{self.name}\' {quantity} * {self.price} = {self.total_price(quantity)}'

    #     Початок коду домашнього завдання №2
    def __add__(self, other):
        """
        реалізація математичного оператора + для екземплярів класу Product.

        :param other: екземпляр класу або Product або ShoppingCart
        :return: екземпляр класу  ShoppingCart
        """
        logger.info(f'call {self.__class__}.__add__ with self={self}, other={other}')
        if isinstance(other, Product):
            cart: ShoppingCart = ShoppingCart()
            cart.add(self, 1)
            cart.add(other, 1)
            return cart
        elif isinstance(other, ShoppingCart):
            other.add(self, 1)
        else:

            msg = f'operation __add__ not implement for {type(self)} and {type(other)}'
            logger.error(msg, exc_info=True)
            raise ProductArithOperError(msg)

    def __mul__(self, other: Union[int, float]):
        """
        Метод __mul__ реалізовує математичну операцію * над продуктом.
        Застосування до продукту цієї операції створює кошик з продуктом self
        c кількістю продукту other.
        Реалізація цього методу дозволяє створювати кошик такими записами:
        cart = pr1*5+pr2+pr3*0.75

        :param other: другий множник типу або int або float
        :return: екземпляр класу ShoppingCart
        """
        logger.info(f'call {self.__class__}.__mul__ with self={self}, other={other}')
        if isinstance(other, (int, float)):
            cart: ShoppingCart = ShoppingCart()
            cart.add(self, other)
            return cart
        else:
            msg = f'operation __mul__  not implement for {type(self)} and {type(other)}'
            logger.error(msg, exc_info=True)
            raise ProductArithOperError(msg)

    def __sub__(self, other):
        """
        Метод реалізує  математичну операцію над екземпляром класу Product.
        Цей метод дозволяє реалізовувати операції такого виду:
        prod1*5-prod1 або prod1*3-prod2
        :param other: екземпляр класу Product. Інший тип не допускається
        :return: екземпляр класу ShoppingCart
        """
        logger.info(f'call {self.__class__}.__sub__ with self={self}, other={other}')
        if isinstance(other, Product):
            cart = ShoppingCart()
            cart.add(self, 1)
            cart.add(other, -1)
            return cart
        else:
            msg = f'operation __sub__  not implement for {type(self)} and {type(other)}'
            logger.error(msg)
            raise ProductArithOperError(msg)

    def __hash__(self) -> int:
        """
        Функція необхідна для реалізації множинності (set) екземплярів класу Product
        :return: хеш-функцію від ключів екземпляру класу
        """
        logger.info(f'call {self.__class__}.__hash__ with self={self}')
        return hash((self.name, self.price))

    def __repr__(self):
        return f"<Product(name, price)>"

    def __str__(self):
        return f"{self.name}, {self.price}"

    def __float__(self):
        logger.info(f'call {self.__class__}.__float__ with self={self}')
        return round(self.price, 2)


class ShoppingCart:
    """
    Клас "Кошик з товарами" реалізує функціонал кошику з товарами для магазина.
    Клас містить такі атрибути:
        products - список екземплярів класу Product
        quantity - список кількості відповідного продукту у кошику
    Продукту з індексом "і" відповідає кількість продукту у списку quantity за індексом і.
    Список products не може містити дублікати екземплярів класу Product.
    Список quantity не може містити кількість продукту менше або рівного нулю, такий
    продукт зі списку products видаляється.

    Методи класу дозволяють визначати вартість кошику, додавати продукт до кошика,
    виконувати арифметичні операції над кошиками
    """

    def __init__(self):
        self.products: List[Product] = []
        self.quantity: List[Union[int, float]] = []

    def is_empty(self) -> bool:
        """
        Метод здійснює перевірку на пустоту кошика
        для майбутнього використання
        :return:
        """
        return not self.products

    def get_num_goods(self) -> int:
        """
        Повертає кількість продуктів у кошику
        для майбутнього використання
        :return: кількість продуктів у кошику
        """
        return len(self.products)

    def get_quantity(self, product: Product) -> Union[int, float]:
        """
        Метод повертає кількість продукту product у кошику
        якщо такого продукту у кошику немає, то повертається нуль
        :param product: екземпляр класу Product
        :return: кількість продукту Union[int, float]
        """
        logger.info(f'call {self.__class__}.get_quantity  with self={self}, product={product}')
        try:
            return self.quantity[self.products.index(product)]
        except ValueError:
            msg = f'продукту немає у списку, product name {product.name}'
            print(msg)
            logger.error(msg)

    def add(self, product_inst: Product, quantity) -> None:
        """
        метод додає продукт у кошик
        :param product_inst: екз класу Product
        :param quantity: кількість продукту
        :return:
        """

        logger.info(f'call {self.__class__}.add  with self={self}, product_inst={product_inst},'
                    f'quantity={quantity}')
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
        :param product: екземпляр класу Product
        :return: None
        """
        i = self.products.index(product)
        self.products.pop(i)
        self.quantity.pop(i)

    def total_price(self) -> float:
        """
        Обраховується вартість кошику
        :return: вартість кошику
        """
        total = 0
        for product, quantity in zip(self.products, self.quantity):
            total += product.total_price(quantity)

        return round(total, 2)

    def __str__(self):
        """
        Строкове відображення кошику
        :return: повертає строку - строкове відображення кошику
        """
        res_str = [f'\nShoppingCart id = {id(self)}']
        if self.products:
            for product, quantity in zip(self.products, self.quantity):
                res_str.append(product.total_price_str(quantity))
            res_str.append('-' * 20)
            res_str.append('total {0}'.format(self.total_price()))
        else:
            res_str.append('shopping cart is empty')
        res_str = '\n'.join(res_str)

        return res_str

    def __add__(self, other):
        """
        реалізація математичного оператора + для екземпляру класу ShoppingCart
        :param other: екземпляр або класу ShoppingCart або класу Product
        :return: екземпляр класу ShoppingCart
        """
        if isinstance(other, Product):
            self.add(other, 1)
            return self
        elif isinstance(other, ShoppingCart):
            new_cart = ShoppingCart()
            new_cart.products = self.products.copy()
            new_cart.quantity = self.quantity.copy()
            for product, quantity in zip(other.products, other.quantity):
                new_cart.add(product, quantity)
            return new_cart
        else:
            msg = f'operation __add__ not implemented for {type(self)} and {type(other)}'
            logger.error(msg)
            raise ProductArithOperError(msg)

    def __sub__(self, other):
        """
        реалізація математичного оператора - для екземпляру класу ShoppingCart
        :param other: екземпляр або класу ShoppingCart або класу Product
        :return: екземпляр класу ShoppingCart
        """
        if isinstance(other, Product):
            self.add(other, -1)
            return self
        elif isinstance(other, ShoppingCart):
            logger.debug(f' other is ShoppingCart')
            logger.debug(f' other quantity before list(map(lambda x: x * -1, other.quantity) - '
                         f'other = {other}')

            other.quantity = list(map(lambda x: x * -1, other.quantity))
            logger.debug(f' after quantity before list(map(lambda x: x * -1, other.quantity)- '
                         f'other = {other}')
            res_cart = self.__add__(other)
            logger.debug(f' {res_cart}')

            return res_cart
        else:
            msg = f'operation __sub__ not implemented for {type(self)} and {type(other)}'
            logger.info(msg)
            raise ProductArithOperError(msg)

    def __repr__(self):
        return f"<ShoppingCart()>"

    def __float__(self):
        return round(self.total_price(), 2)


# і тут замовник каже: зроби функціонал з дісконтом

class ProductDiscount(Product):

    def __init__(self, name: str, price: Union[int, float], discount: Union[int, float],
                 rules: Union[int, float]) -> None:
        """

        :param name: назва продукту, унікальне
        :param price: вартість одиниці продукту
        :param discount: знижка у відсотках
        :param rules: правила застосування знижки, кількість одиниць товару, з якої починається дісконт
        """
        super().__init__(name, price)
        self.discount = discount
        self.rules = rules

    def discount_count(self, quantity: Union[int, float]) -> Union[int, float]:
        """
        Метод обраховує розмір знижки
        :param quantity: кількість товару
        :return: розмір знижки
        """
        if quantity > self.rules:
            discount = round(self.price / 100 * self.discount, 2)
        else:
            discount = 0
        return discount

    def total_price(self, quantity: Union[int, float]) -> Union[int, float]:
        return round(super().total_price(quantity) - self.discount_count(quantity), 2)

    def total_price_str(self, quantity) -> str:

        res_str = [f'\'{self.name}\' {quantity} * {self.price} = {super().total_price(quantity)}']
        # якщо дісконт більше нуля, то відображаємо його у "квитанції"
        if self.discount_count(quantity) > 0:
            res_str.append(f'discount -{self.discount_count(quantity)}'.rjust(len(res_str[0]), " "))
            res_str.append(f'total {self.total_price(quantity):>}'.rjust(len(res_str[0]), " "))
        return '\n'.join(res_str)


if __name__ == '__main__':
    logger.debug('start script')

    # create products
    tomato = Product('tomato', 34.50)
    tomato1 = Product('tomato', 15.50)
    mango = Product('mango', 60.50)
    beef = Product('beef', 50)

    # test Product operation
    print('\n test Product operation tomato*5 - tomato + mango + mango - beef')
    res = tomato - tomato * 5 + mango - mango - beef
    print(res)
