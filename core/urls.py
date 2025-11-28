from rest_framework.routers import DefaultRouter
from .views import SocioViewSet, ProductoViewSet

router = DefaultRouter()
router.register(r'socios', SocioViewSet, basename='socio')
router.register(r'productos', ProductoViewSet, basename='producto')

urlpatterns = router.urls
