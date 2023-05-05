from rest_framework.exceptions import APIException

class NotInStock(APIException):
    status_code = 400
    default_detail = "We don't have this quantity in stock"
    default_code = "not_in_stock"
