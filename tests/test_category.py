import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.db.models import Q
from django.core.exceptions import ValidationError

from . import TomatoTest
from wallet.serializers import CategorySerializer
from wallet.views import CategoryViewSet
from wallet.models import Category


class CategoryTest(TomatoTest):
    def setUp(self):
        super().setUp()

    def test_list_anonymousUser(self):
        response = self.client.get('/category/')
        self.assertEqual(response.status_code, 403)

    def test_list(self):
        # tes_create_andt category list shows only categroies with no owner or
        # owner is current user.
        Category.objects.create(name='default')
        Category.objects.create(name='sbs category', owner=self.sb)
        Category.objects.create(name='tomatos category', owner=self.user)

        self.assertTrue(self.client.login(**self.user_info))
        response = self.client.get('/category/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['count'], 2)

        serializer = CategorySerializer(
            Category.objects.filter(
                Q(owner__isnull=True) |
                Q(owner=self.user)).order_by('-created_at'),
            many=True)
        serializer_data = json.loads(json.dumps(serializer.data))
        response_data = json.loads(response.content)['results']

        # check the fields
        self.assertListEqual(
            list(response_data[0].keys()),
            ['id', 'name', 'owner'])

        # check the data
        self.assertEqual(serializer_data, response_data)

    def test_create_anonymousUser(self):
        response = self.client.post('/category/', self.cdict, format='json')
        self.assertEqual(response.status_code, 403)

    def test_create_empty_name(self):
        # test category name can't be empty
        self.assertTrue(self.client.login(**self.user_info))
        response = self.client.post('/category/', {'name': ''}, format='json')
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/category/', {'name': None}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create(self):
        self.assertTrue(self.client.login(**self.user_info))
        response = self.client.post('/category/', self.cdict, format='json')
        self.assertEqual(response.status_code, 201)
        serializer = CategorySerializer(Category.objects.get(owner=self.user, name=self.cname))
        self.assertEqual(
            json.loads(json.dumps(serializer.data)),
            json.loads(response.content))

        # check all fof the fields needed in the results.
        self.assertListEqual(
            list(json.loads(response.content).keys()),
            ['id', 'name', 'owner'])

    def test_retrieve(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass

    def test_model_duplicate(self):
        # test create duplicate category with no owner
        Category.objects.create(name='default')
        self.assertEqual(Category.objects.count(), 1)
        with self.assertRaises(ValidationError):
            Category.objects.create(name='default')

        # test create duplicate category with owner
        Category.objects.create(name='default', owner=self.user)
        self.assertEqual(Category.objects.count(), 2)
        with self.assertRaises(ValidationError):
            Category.objects.create(name='default', owner=self.user)
