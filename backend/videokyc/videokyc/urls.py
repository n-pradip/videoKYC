from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('kyc.urls')),
    path('accounts/',include('accounts.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = f"{settings.COMPANY_NAME}"
admin.site.site_title = f"{settings.COMPANY_NAME}"
admin.site.index_title = f"Welcome to {settings.COMPANY_NAME}"
admin.site.site_header = f"{settings.COMPANY_NAME}"