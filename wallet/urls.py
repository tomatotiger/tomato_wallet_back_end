from django.urls import path, include
from rest_framework import routers

from wallet.views import CategoryViewSet, ExpenseViewSet


router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'expense', ExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
