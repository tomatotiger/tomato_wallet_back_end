import json

from . import TomatoTest
from wallet.models import Category


class CategoryTest(TomatoTest):

    def test_not_allow_anonymousUser(self):
        # anonymous user visit list API
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 403)

    def test_list(self):
        Category.objects.create(name='c1')
        Category.objects.create(name='c2')
        Category.objects.create(name='c3')

        self.assertTrue(self.client.login(**self.user_info))
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(json.loads(response.content)['count'], 3)
        response_data = json.loads(response.content)['results']
        self.assertListEqual(list(response_data[0].keys()), ['id', 'name'])
        self.assertEqual([c['name'] for c in response_data], ['c3', 'c2', 'c1'])
