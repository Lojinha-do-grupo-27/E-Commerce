from rest_framework.exceptions import APIException

class NotInStock(APIException):
    status_code = 400
    default_detail = "We don't have this quantity in stock"
    default_code = "not_in_stock"

    def __init__(self, detail=None):
        if detail is None:
            detail = self.default_detail
        self.detail = detail

class AlreadyInCart(APIException):
    status_code = 400
    default_detail = "This product already added in the cart"
    default_code = "error"