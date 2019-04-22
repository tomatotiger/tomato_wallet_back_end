from rest_framework import serializers
from wallet.models import Category, Expense


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Category
        fields = ('parent', 'name', 'owner')


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Expense
        fields = ('amount', 'category', 'record_time', 'owner')
