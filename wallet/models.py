from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(blank=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Category)
def validate_unique(sender, instance, **kwargs):
    # unique_together of parent, name and owner
    if Category.objects.filter(owner=instance.owner, name=instance.name).exists():
        raise ValidationError("Duplicate Category")


def get_sentinel_category():
    return Category.objects.get_or_create(name='Default')[0]


class Expense(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET(get_sentinel_category))
    record_time = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
