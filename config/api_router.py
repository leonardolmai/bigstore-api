from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from bigstore_api.users.api.views import CompanyViewSet, UserViewSet
from bigstore_api.infouser.api.views import CardViewSet
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("companies", CompanyViewSet)
router.register("cards", CardViewSet)

app_name = "api"
urlpatterns = router.urls
