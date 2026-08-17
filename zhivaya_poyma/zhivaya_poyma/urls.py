from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from news.ckeditor_views import ckeditor_image_upload

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import urls as wagtail_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("join/", include("leads.urls")),

    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),

    path("news/", include(wagtail_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
