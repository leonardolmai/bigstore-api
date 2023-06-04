from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from bigstore_api.cards.api.views import CardViewSet
from bigstore_api.products.api.views import ProductViewSet
from bigstore_api.users.api.views import CompanyViewSet, UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("companies", CompanyViewSet)
router.register("products", ProductViewSet)

router.register("cards", CardViewSet)


app_name = "api"
urlpatterns = router.urls
