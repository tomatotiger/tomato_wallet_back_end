from django.urls import path, include
from rest_framework import routers

from wallet.views import CategoryListViewSet, ExpenseViewSet


router = routers.DefaultRouter()
router.register(r'categories', CategoryListViewSet, basename='categories')
router.register(r'expense', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
