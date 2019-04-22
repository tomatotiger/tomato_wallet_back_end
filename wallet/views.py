from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets


from wallet.models import Category, Expense
from wallet.serializers import CategorySerializer, ExpenseSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-created_at')
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
