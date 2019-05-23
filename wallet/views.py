from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from wallet.models import Category, Expense
from wallet.serializers import CategorySerializer, ExpenseSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Category.objects.all().order_by('-id')


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Expense.objects.filter(
            owner=self.request.user
        ).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
