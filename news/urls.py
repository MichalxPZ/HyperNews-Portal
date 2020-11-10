from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'index'),
    path('news/', views.mainpage, name = 'mainpage'),
    path('news/<int:numer>/', views.news, name = 'news'),
    path('news/create/', views.create, name = 'create'),
]
urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)