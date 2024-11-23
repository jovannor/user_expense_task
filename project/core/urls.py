from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter

from accounts.views import (
    UserRetrieveView,
    UserListView,
    UserTransactionsHistoryView,
    ExpenseViewSet,
    IncomeViewSet,
    UserExpenseCategorySumView
)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="User expense project description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

doc_urls = [
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

router = DefaultRouter()
router.register(r'expense', ExpenseViewSet, basename='expense')
router.register(r'income', IncomeViewSet, basename='income')

user_urls = [
    path("users/", UserListView.as_view()),
    path("users/<int:user_id>/", UserRetrieveView.as_view()),
    path("users/<int:user_id>/category-summary/", UserExpenseCategorySumView.as_view()),
    path("users/<int:user_id>/transactions/", UserTransactionsHistoryView.as_view()),
    path("users/<int:user_id>/", include(router.urls)),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v0/", include(user_urls)),
    path("api/v0/", include(doc_urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
