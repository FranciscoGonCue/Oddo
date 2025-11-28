from rest_framework.routers import DefaultRouter
from .views import OrdenPOSViewSet, LineaOrdenPOSViewSet

router = DefaultRouter()
router.register(r'ordenes-pos', OrdenPOSViewSet, basename='orden-pos')
router.register(r'lineas-orden-pos', LineaOrdenPOSViewSet, basename='linea-orden-pos')

urlpatterns = router.urls
