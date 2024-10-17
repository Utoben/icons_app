from django.urls import path
from django.conf import settings

from . import views
from django.conf.urls.static import static

urlpatterns = [
    
    # страницы
    path('', views.home, name='home'),
    path('bucket/', views.bucket_view, name='bucket'),
    path('choise/', views.choise, name='choise'),
    path('clear_bucket/', views.clear_bucket, name='clear_bucket'),
    path('get_profile_info/', views.get_profile_info, name='get_profile_info'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)