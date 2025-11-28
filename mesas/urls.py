from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'mesas', views.MesaViewSet, basename='mesa')
router.register(r'sesiones-mesa', views.SesionMesaViewSet, basename='sesion-mesa')

urlpatterns = [
    path('', views.index, name='mesas-index'),
] + router.urls
