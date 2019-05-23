from rest_framework import viewsets
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from django.views.defaults import bad_request
from rest_framework import mixins

from wallet.models import Category, Expense
from wallet.serializers import CategorySerializer, ExpenseSerializer


class CategoryListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Category.objects.all().order_by('-created_at')


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Expense.objects.filter(
            owner=self.request.user
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
