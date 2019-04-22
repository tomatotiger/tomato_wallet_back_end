from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(blank=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


def get_sentinel_category():
    return Category.objects.get_or_create(name='default')[0]


class Expense(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    amount = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.SET(get_sentinel_category))
    record_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
