import json
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from wallet.models import Category, Expense


class TomatoTest(APITestCase):
    def setUp(self):
        self.user_info = {'username': 'tomato', 'password': 'top_secret'}
        self.user = User.objects.create_user(**self.user_info)

        self.sb_info = {'username': 'somebody', 'password': 'top_secret'}
        self.sb = User.objects.create_user(**self.sb_info)

        self.cname = 'category'
        self.cdict = {'name': 'category'}
