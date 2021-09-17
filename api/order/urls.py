from rest_framework import routers, urlpatterns, viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'', views.OrderViewSet)

urlpatterns = [
    path('add/<str:id>/<str:token>/',views.add, name='order.add'),
    path('',include(router.urls))
]