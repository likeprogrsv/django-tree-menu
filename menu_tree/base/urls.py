from django.urls import path, re_path, include
from .views import index
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', index, name='home'),
    re_path(r'^(?P<path>.+)/$', index, name='categories'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
