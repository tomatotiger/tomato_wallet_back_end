import json

from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.db.models import Q

from . import TomatoTest
from wallet.serializers import ExpenseSerializer
from wallet.views import ExpenseViewSet
from wallet.models import Category, Expense


class ExpenceTest(TomatoTest):
    def setUp(self):
        super().setUp()
        self.no_owner_cate = Category.objects.create(name=self.cname)
        self.cate = Category.objects.create(name=self.cname, owner=self.user)

    def test_list_anonymousUser(self):
        response = self.client.get('/expense/')
        self.assertEqual(response.status_code, 403)

    def test_list(self):
        now = timezone.now()
        Expense.objects.create(amount=1,
                               owner=self.user,
                               category=self.cate,
                               record_time=now)
        Expense.objects.create(amount=2,
                               owner=self.sb,
                               category=self.cate,
                               record_time=now)
        Expense.objects.create(amount=3,
                               owner=self.user,
                               category=self.no_owner_cate,
                               record_time=now)

        self.assertTrue(self.client.login(**self.user_info))
        response = self.client.get('/expense/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['count'], 2)

        serializer = ExpenseSerializer(
            Expense.objects.filter(owner=self.user).order_by('-created_at'),
            many=True)
        serializer_data = json.loads(json.dumps(serializer.data))
        response_data = json.loads(response.content)['results']

        # check the fields
        self.assertListEqual(list(response_data[0].keys()),
                             ['id', 'amount', 'category', 'record_time'])

        # check the data
        self.assertEqual(serializer_data, response_data)

    def test_create_anonymousUser(self):
        response = self.client.post('/expense/', {}, fomat='json')
        self.assertEqual(response.status_code, 403)

    def test_create_amount_0(self):
        self.assertTrue(self.client.login(**self.user_info))
        response = self.client.post(
            '/expense/',
            {'amount': 0, 'category_name': 'c'},
            format='json')
        self.assertEqual(response.status_code, 400)

    def test_create_empty_category(self):
        self.assertTrue(self.client.login(**self.user_info))
        response = self.client.post('/expense/', {'amount': 0}, format='json')
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            '/expense/', {'amount': 0, 'category_name': ''}, format='json')
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            '/expense/', {'amount': 0, 'category_name': None}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create(self):
        self.assertTrue(self.client.login(**self.user_info))
        response = self.client.post(
            '/expense/',
            {'amount': 10, 'category_name': 'c'},
            format='json')
        self.assertEqual(response.status_code, 201)

    def test_retrieve_anonymousUser(self):
        response = self.client.post('/expense/', {}, fomat='json')
        self.assertEqual(response.status_code, 403)

    def test_retrieve(self):
        pass

    def test_update_anonymousUser(self):
        pass

    def test_update(self):
        pass

    def test_model_delete_category(self):
        # test create duplicate category with no owner
        Expense.objects.create(category=self.cate, amount=11, owner=self.user)
        self.assertEqual(Expense.objects.count(), 1)
        self.cate.delete()
        self.assertEqual(Expense.objects.first().category.name, 'Default')

    def test_delete_anonymousUser(self):
        pass

    def test_delete(self):
        pass

