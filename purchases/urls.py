from rest_framework.routers import DefaultRouter
from .views import OrdenCompraViewSet, LineaOrdenCompraViewSet

router = DefaultRouter()
router.register(r'ordenes-compra', OrdenCompraViewSet, basename='orden-compra')
router.register(r'lineas-orden-compra', LineaOrdenCompraViewSet, basename='linea-orden-compra')

urlpatterns = router.urls
