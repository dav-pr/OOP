"""
Errors Class
for classes Product and Cart

"""


class ProductError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ProductArithOperError(ProductError):
    def __init__(self, message):
        super().__init__(message)
