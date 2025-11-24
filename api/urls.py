from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ItemViewSet, FacturaViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'facturas', FacturaViewSet, basename='factura')

urlpatterns = [
    path('', include(router.urls)),
]
