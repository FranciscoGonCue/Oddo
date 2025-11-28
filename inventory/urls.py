from rest_framework.routers import DefaultRouter
from .views import AlmacenViewSet, CantidadStockViewSet

router = DefaultRouter()
router.register(r'almacenes', AlmacenViewSet, basename='almacen')
router.register(r'cantidades-stock', CantidadStockViewSet, basename='cantidad-stock')

urlpatterns = router.urls
