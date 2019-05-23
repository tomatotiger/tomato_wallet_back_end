import json

from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.db.models import Q

from . import TomatoTest
from wallet.serializers import ExpenseSerializer
from wallet.views import ExpenseViewSet
from wallet.models import Category, Expense


class ExpenseTest(TomatoTest):

    def test_anonymousUser(self):
        # test_get_by_anonymous
        response = self.client.get('/expense/')
        self.assertEqual(response.status_code, 403)
        response = self.client.get('/expense/1/')
        self.assertEqual(response.status_code, 403)

        # test_create_by_anonymous
        response = self.client.post('/expense/', {}, fomat='json')
        self.assertEqual(response.status_code, 403)

        # test_edit_by_anonymousUser
        response = self.client.put('/expense/1/', {}, fomat='json')
        self.assertEqual(response.status_code, 403)

        # test_destroy_by_anonymousUser
        response = self.client.delete('/expense/1/', {}, fomat='json')
        self.assertEqual(response.status_code, 403)

    def test_create(self):
        self.assertTrue(self.client.login(**self.user_info))
        response = self.client.post(
            '/expense/',
            {'amount': 10, 'category_name': 'c'},
            format='json')
        self.assertEqual(response.status_code, 201)

        # created a new category named c
        self.assertEqual(Category.objects.all().count(), 1)
        self.assertEqual(Category.objects.first().name, 'c')

        self.assertEqual(Expense.objects.all().count(), 1)
        self.assertEqual(Expense.objects.first().owner, self.user)
        self.assertEqual(Expense.objects.first().amount, 10)
        self.assertEqual(Expense.objects.first().category.name, 'c')

    def test_create_amount_0(self):
        self.assertTrue(self.client.login(**self.user_info))
        response = self.client.post(
            '/expense/',
            {'amount': 0, 'category_name': 'c'},
            format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Category.objects.all().count(), 0)
        self.assertEqual(Expense.objects.all().count(), 0)

    def test_create_empty_category(self):
        self.assertTrue(self.client.login(**self.user_info))
        response = self.client.post('/expense/', {'amount': 1}, format='json')
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/expense/', {'amount': 2, 'category': ''}, format='json')
        self.assertEqual(response.status_code, 201)

        self.assertEqual(Category.objects.all().count(), 0)
        expenses = Expense.objects.all()
        self.assertEqual(expenses.count(), 2)
        self.assertEqual(expenses[0].amount, 1.00)
        self.assertEqual(expenses[0].category, None)
        self.assertEqual(expenses[0].owner, self.user)
        self.assertEqual(expenses[1].amount, 2.00)
        self.assertEqual(expenses[1].category, None)
        self.assertEqual(expenses[1].owner, self.user)

    def test_list(self):
        now = timezone.now()
        c = Category.objects.create(name='c')
        Expense.objects.create(amount=1,
                               owner=self.user,
                               category=c,
                               record_time=now)
        Expense.objects.create(amount=2,
                               owner=self.sb,
                               record_time=now)
        Expense.objects.create(amount=3,
                               owner=self.user,
                               record_time=now)
        self.assertTrue(self.client.login(**self.user_info))

        response = self.client.get('/expense/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['count'], 2)

        response_data = json.loads(response.content)['results']

        # check the fields
        self.assertListEqual(list(response_data[0].keys()),
                             ['id', 'amount', 'category', 'record_time'])

        # check the data
        self.assertEqual([e['amount'] for e in response_data], ['3.00', '1.00'])

    def test_retrieve(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass

