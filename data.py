class Urls:
    BASE_URL = 'https://stellarburgers.education-services.ru'
    REGISTER = '/api/auth/register'
    LOGIN = '/api/auth/login'
    USER = '/api/auth/user'
    ORDERS = '/api/orders'
    INGREDIENTS = '/api/ingredients'


class Messages:
    USER_ALREADY_EXISTS = 'User already exists'
    REQUIRED_FIELDS = 'Email, password and name are required fields'
    INCORRECT_CREDENTIALS = 'email or password are incorrect'
    INGREDIENTS_REQUIRED = 'Ingredient ids must be provided'


class TestData:
    INVALID_INGREDIENT_HASH = ['invalid_hash_123456789']
    EMPTY_INGREDIENTS = []