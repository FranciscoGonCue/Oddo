from rest_framework.routers import DefaultRouter
from .views import EmpleadoViewSet

router = DefaultRouter()
router.register(r'empleados', EmpleadoViewSet, basename='empleado')

urlpatterns = router.urls
