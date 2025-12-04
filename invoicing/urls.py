from rest_framework.routers import DefaultRouter
from .views import FacturaViewSet, PagoViewSet, LineaFacturaViewSet

router = DefaultRouter()
router.register(r'facturas', FacturaViewSet, basename='factura')
router.register(r'pagos', PagoViewSet, basename='pago')
router.register(r'lineas-factura', LineaFacturaViewSet, basename='linea-factura')

urlpatterns = router.urls
