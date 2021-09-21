from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from api.sitemaps import ProductSitemap
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="Ecommerce Software APIs")


sitemaps = {"product": ProductSitemap}


urlpatterns = [
    path("swagger-docs/", schema_view),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin", admin.site.urls),
    path("api/product/", include("api.urls.product_urls"), name='product'),
    path("api/order/", include("api.urls.order_urls")),
    path("api/user/", include("api.urls.user_urls")),
    # Sitemap Route
    path(
        "sitemap.xml",
        cache_page(86400)(sitemap),
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # Robots.txt Route
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="config/robots.txt", content_type="text/plain"
        ),
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
