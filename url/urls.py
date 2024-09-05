from django.urls import path

from . import views


urlpatterns = [
    path('', views.AddUrlView.as_view(), name='add_url'),
    path('list/', views.UrlListView.as_view(), name='url_list'),
]