

class Constants:
    URL_CREATE_USER = 'https://stellarburgers.nomoreparties.site/api/auth/register'
    SAME_USER = {
    "success": False,
    "message": "User already exists"
    }
    BODY_NO_FIELD = {
    "success": False,
    "message": "Email, password and name are required fields"
    }
    URL_LOGIN_USER = 'https://stellarburgers.nomoreparties.site/api/auth/login'
    BODY_WRONG_DATA = {
    "success": False,
    "message": "email or password are incorrect"
    }
    URL_CHANGE_USER = 'https://stellarburgers.nomoreparties.site/api/auth/user'
    BODY_NOT_AUTH = {
    "success": False,
    "message": "You should be authorised"
    }
    URL_ORDER = 'https://stellarburgers.nomoreparties.site/api/orders'
    BODY_NO_INGRIDIENT = {
    "success": False,
    "message": "Ingredient ids must be provided"
    }
    URL_DELETE = 'https://stellarburgers.nomoreparties.'

