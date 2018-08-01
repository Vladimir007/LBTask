import random
from datetime import datetime
from rest_framework.test import APIClient
from shop.models import User, Product, DocumentType, Store, AccessGroup


USERS = [
    {
        'username': 'admin',
        'first_name': 'Владимир',
        'last_name': 'Гратинский',
        'patronymic': 'Анатольевич',
        'password': '12345',
        'is_staff': True
    },
    {
        'username': 'manager',
        'first_name': 'Мария',
        'last_name': 'Кравец',
        'patronymic': 'Сергеевна',
        'password': '12345'
    },
    {
        'username': 'inspector',
        'first_name': 'Олег',
        'last_name': 'Гратинский',
        'patronymic': 'Анатольевич',
        'password': '12345'
    },
    {
        'username': 'guest',
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'patronymic': 'Иванович',
        'password': '12345'
    },
]

DOC_TYPES = ['Приказ', 'Протокол', 'Акт', 'Докладная', 'Распоряжение', 'Постановление']

STORES = [
    'Магнит', 'Пятерочка', 'Avito', 'Евросеть', 'Связной', 'М.Видео', 'DNS shop', 'Мегафон',
    'Билайн', 'МТС', 'OZON.ru', 'Ситилинк', 'Цифроград', '123.ru'
]

PRODUCTS = [
    'Milk', 'Bread', 'Butter', 'Coffee', 'Fish', 'Pork', 'Salt', 'Pepper', 'Onion', 'Orange', 'Oil', 'Potato',
    'Asparagus', 'Broccoli', 'Carrot', 'Cucumbers', 'Garlic', 'Ginger', 'Tomatoes', 'Bean', 'Avocado', 'Bananas',
    'Strawberry', 'Oats', 'Coconut', 'Peanut', 'Cheese', 'Eggs', 'Salmon', 'Tuna', 'Shrimp', 'Yogurt', 'Almond'
]

DOCUMENTS = [
    {
        'doc_type': 0,
    }
]


class Populate:
    def __init__(self, r_seed=888):
        random.seed(r_seed)
        self.users = []
        self.client = APIClient()
        if len(self.users) != 4 and User.objects.all().count() == 0:
            self.create_users()
        elif len(self.users) != 4:
            self.users = [User.objects.get(username='admin'), User.objects.get(username='manager'),
                          User.objects.get(username='inspector'), User.objects.get(username='guest')]

    def login(self, **kwargs):
        resp = self.client.login(**kwargs)
        assert resp is True

    def create_users(self):
        for user in USERS:
            is_staff = user.pop('is_staff', False)
            if is_staff:
                self.users.append(User.objects.create_superuser(**user))
            else:
                self.users.append(User.objects.create_user(**user))

    def clear_shop_tables(self):
        Store.objects.all().delete()
        Product.objects.all().delete()
        DocumentType.objects.all().delete()
        AccessGroup.objects.all().delete()

    def fill_stores(self):
        stores = []
        for store in STORES:
            resp = self.client.post('/shop-api/stores/', {'name': store}, format='json').json()
            assert 'id' in resp
            stores.append(resp['id'])
        return stores

    def fill_products(self):
        products = []
        for product in PRODUCTS:
            resp = self.client.post('/shop-api/products/', {'name': product}, format='json').json()
            assert 'id' in resp
            products.append(resp['id'])
        return products

    def fill_doctypes(self):
        doctypes = []
        for doc_type in DOC_TYPES:
            resp = self.client.post('/shop-api/doctypes/', {'name': doc_type}, format='json').json()
            assert 'id' in resp
            doctypes.append(resp['id'])
        return doctypes

    def fill_documents(self, number):
        doctypes = self.fill_doctypes()
        self.create_access_groups(doctypes)

        stores = self.fill_stores()
        products = self.fill_products()

        documents = []
        for i in range(number):
            document_args = {
                'store': random.choice(stores),
                'doc_type': random.choice(doctypes),
                'doc_date': self.get_random_date(),
            }
            resp = self.client.post('/shop-api/documents/', document_args, format='json').json()
            assert 'id' in resp
            documents.append(resp['id'])

        for d_id in documents:
            doc_products = random.sample(products, random.randint(1, len(products)) // 3)
            for p_id in doc_products:
                docproducts_args = {'document': d_id, 'product': p_id, 'number': random.randint(1, 100)}
                self.client.post('/shop-api/docproducts/', docproducts_args, format='json').json()

        return len(documents)

    def create_access_groups(self, doctypes):
        resp = self.client.post('/shop-api/accessgroup/', {
            'name': 'Administrator', 'doctypes': doctypes
        }, format='json').json()
        assert 'id' in resp
        self.users[0].group_id = resp['id']
        self.users[0].save()

        resp = self.client.post('/shop-api/accessgroup/', {
            'name': 'Inspector', 'doctypes': random.sample(doctypes, random.randint(1, len(doctypes)))
        }, format='json').json()

        assert 'id' in resp
        self.users[1].group_id = resp['id']
        self.users[1].save()

        resp = self.client.post('/shop-api/accessgroup/', {
            'name': 'Manager', 'doctypes': [random.choice(doctypes)]
        }, format='json').json()
        assert 'id' in resp
        self.users[2].group_id = resp['id']
        self.users[2].save()


    def get_random_date(self):
        year = random.randint(1990, 2018)
        month = random.randint(1, 12)
        if month == 2:
            max_day = 28
        elif month in {1, 3, 5, 7, 8, 10, 12}:
            max_day = 31
        else:
            max_day = 30
        day = random.randint(1, max_day)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        # '%B %d, %Y %H:%M %p'
        return datetime(year, month, day, hour, minute).isoformat()


def fill_database(number):
    p = Populate()
    p.login(username='admin', password='12345')
    p.clear_shop_tables()
    num = p.fill_documents(number)
    p.client.logout()
    return num
