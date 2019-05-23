from rest_framework import serializers
from wallet.models import Category, Expense


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = Category
        fields = ('id', 'name')


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(read_only=True)
    category_name = serializers.CharField(write_only=True, required=False)
    record_time = serializers.DateTimeField(required=False)

    class Meta:
        model = Expense
        fields = ('id', 'amount', 'category', 'category_name', 'record_time')

    def validate(self, data):
        if data['amount'] == 0:
            raise serializers.ValidationError("amount can not be 0")
        return data

    def create(self, validated_data):
        cname = validated_data.pop('category_name', None)
        if cname:
            category = Category.objects.get_or_create(name=cname)[0]
            expense = Expense.objects.create(**validated_data, category=category)
        else:
            expense = Expense.objects.create(**validated_data)
        return expense
