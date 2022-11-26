from typing import Union


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
        return True if self.name and self.price > 0 else False

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

        return True if isinstance(other, Product) and self.name == other.name and self.price == other.price else False

    def __ne__(self, other) -> bool:
        if isinstance(other, Product):
            return True if self.name != other.name or self.price != other.price else False
        else:
            raise ProductError('none copmare object, type mismatch')

    def total_price_str(self, quantity) -> str:
        """
        метод повертає строку-формулу розрахунку вартості
        :param quantity:
        :return: str - формулf розрахунку вартості
        """

        el_of_str = [self.name, quantity, self.price, self.total_price(quantity)]
        return '\'{0}\' {1} * {2} = {3}'.format(*el_of_str)


class ShoppingCart:
    """
    клас "Корзина з товарами"
    """

    def __init__(self):

        self.products: list[Product] = []
        self.quantity: list[Union[int, float]] = []

    def is_empty(self) -> bool:
        """
        для майбутнього використання
        :return:
        """
        return True if not len(self.products) else False

    def get_num_goods(self) -> int:
        """
        для майбутнього використання
        :return:
        """
        return len(self.products)

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
            for i, product in enumerate(self.products):
                if product == product_inst:
                    self.quantity[i] += quantity

    def pop(self, index: int) -> None:
        """
        видаляє із списків self.products та self.quantity
        елементи з індексом index
        :param index: індекс елементу
        :return: None
        """
        self.products.pop(index)
        self.quantity.pop(index)

    def rm(self, product_inst: Product, quantity=0) -> None:
        """
        зменьшує кількість товару Product у корзина на кількість quantity
        Якщо quantity = 0, то видаляеться увест товар Product із корзини
        Якщо кількість товару, що в результаті зменьшення = 0, то товар видаляеться із корзини
        :param product_inst:
        :param quantity:
        :return:
        """
        if product_inst in self.products:
            for i, product in enumerate(self.products):
                if product == product_inst:
                    if quantity == 0:
                        self.pop(i)
                    else:
                        if self.quantity[i] < quantity:
                            self.pop(i)
                        else:
                            self.quantity[i] -= quantity

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
        return super().total_price(quantity) - self.discont_count(quantity)

    def total_price_str(self, quantity) -> str:

        res_str = []
        el_of_str = [self.name, quantity, self.price, super().total_price(quantity)]
        res_str.append('\'{0}\' {1} * {2} = {3}'.format(*el_of_str))
        # якщо дісконт більше нуля, то відображаемо його у "квитанції"
        if self.discont_count(quantity) > 0:
            res_str.append('discont -{0}'.format(self.discont_count(quantity)).rjust(len(res_str[0]), " "))
            res_str.append('total {0}'.format(self.total_price(quantity)).rjust(len(res_str[0]), " "))
        return '\n'.join(res_str)


if __name__ == '__main__':
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
    cart.rm(tomato, 0.5)
    print(cart)

    tomato_disc = ProductDiscont("milk", 14.5, discont=10, rules=8)
    cart.add(tomato_disc, 9)
    print(cart)
