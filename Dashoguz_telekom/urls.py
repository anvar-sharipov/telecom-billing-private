from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('chat/', include('chat.urls')),
    path('', include('telekom.urls')),
]

urlpatterns += static('/favicon.ico', document_root=settings.STATIC_ROOT)
# раздача media в dev (на сервере /media отдаёт Apache через Alias)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
