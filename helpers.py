import random
import string

from faker import Faker

fake = Faker()


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_user_data():
    return {
        'email': f'{generate_random_string()}@yandex.ru',
        'password': generate_random_string(12),
        'name': fake.first_name()
    }