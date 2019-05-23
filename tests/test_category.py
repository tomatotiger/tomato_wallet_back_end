import json
from django.db.utils import IntegrityError

from . import TomatoTest
from wallet.models import Category


class CategoryTest(TomatoTest):
    def setUp(self):
        super().setUp()

    def test_model_name_duplicate(self):
        Category.objects.create(name='c')
        self.assertEqual(Category.objects.count(), 1)
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='c')

    def test_not_allow_anonymousUser(self):
        # anonymous user create category API
        response = self.client.post('/category/', {'name': 'c'}, format='json')
        self.assertEqual(response.status_code, 403)

        # anonymous user visit list API
        response = self.client.get('/category/')
        self.assertEqual(response.status_code, 403)

    def test_create_with_empty_name(self):
        self.assertTrue(self.client.login(**self.user_info))
        response = self.client.post('/category/', {'name': ''}, format='json')
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/category/', {'name': None}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create(self):
        self.assertTrue(self.client.login(**self.user_info))
        response = self.client.post('/category/', {'name': 'c'}, format='json')
        self.assertEqual(response.status_code, 201)

        self.assertEqual(Category.objects.filter(name='c').count(), 1)

        # check all fof the fields needed in the results.
        self.assertListEqual(
            list(json.loads(response.content).keys()), ['id', 'name'])

        self.assertEqual(json.loads(response.content)['name'], 'c')

    def test_list(self):
        Category.objects.create(name='c1')
        Category.objects.create(name='c2')
        Category.objects.create(name='c3')

        self.assertTrue(self.client.login(**self.user_info))
        response = self.client.get('/category/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(json.loads(response.content)['count'], 3)
        response_data = json.loads(response.content)['results']
        self.assertListEqual(list(response_data[0].keys()), ['id', 'name'])
        self.assertEqual([c['name'] for c in response_data], ['c3', 'c2', 'c1'])

    def test_retrieve(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass
