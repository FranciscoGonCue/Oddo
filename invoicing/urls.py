from rest_framework.routers import DefaultRouter
from .views import FacturaViewSet, PagoViewSet

router = DefaultRouter()
router.register(r'facturas', FacturaViewSet, basename='factura')
router.register(r'pagos', PagoViewSet, basename='pago')

urlpatterns = router.urls
