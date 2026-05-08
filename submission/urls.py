from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import *

# -----------------------------
# Swagger Configuration
# -----------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="Blood Donation API",
        default_version="v1",
        description="CRUD APIs for Blood Donation System",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# -----------------------------
# Router Configuration
# -----------------------------
router = DefaultRouter()
router.register(r'users', UserViewSet, basename="users")
router.register(r'health-status', HealthStatusViewSet, basename="health-status")
router.register(r'requests', RequestViewSet, basename="requests")

# -----------------------------
# URL Patterns
# -----------------------------
urlpatterns = [
    # # Router URLs (CRUD)
    # path("api/", include(router.urls)),

    # # Custom APIs
    path("api/donors/search/", DonorSearchAPIView.as_view(), name="donor-search"),
    # path(
    #     "api/health-status/user/<str:user_id>/",
    #     HealthStatusByUserAPIView.as_view(),
    #     name="health-status-by-user"
    # ),
    # path(
    #     "api/requests/<str:request_id>/status/",
    #     UpdateRequestStatusAPIView.as_view(),
    #     name="update-request-status"
    # ),

     # Swagger URLs
    path(
       "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-ui",
    ),
    # path(
    #     "redoc/",
    #     schema_view.with_ui("redoc", cache_timeout=0),
    #     name="redoc",
    # ),
    path(
        "donor/", donors, name="donor"
    ),
    path(
        "", home, name="home"
    ),
    path(
        "contact/", contact, name="contact"
    ),
    path(
        "request/", request, name="request"
    ),
    path(
        "register/", register, name="register"
    ),
    path(
        "login/", login, name="login"
    ),
    path("add-donor/", add_donor, name="add-donor"),
    path("api/add-donor/", add_donor, name="api-add-donor"),
    
    
]
