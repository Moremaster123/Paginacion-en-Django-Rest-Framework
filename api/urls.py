from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('users', UserViewSet, basename='user')

urlpatterns = router.urls
