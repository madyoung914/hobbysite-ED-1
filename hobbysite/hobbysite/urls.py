from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('user_management.urls', namespace='profile')),
    path('', include('main_interface.urls', namespace='main')),
    path('forum/', include('forum.urls', namespace="forum")),
    path('merchstore/', include('merchstore.urls', namespace='merchstore')),
    path('wiki/', include('wiki.urls', namespace="wiki")),
    path('commissions/', include('commissions.urls', namespace="commissions")),
    path('blog/', include('blog.urls', namespace="blog")),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
