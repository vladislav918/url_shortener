from django.urls import path

from . import views


urlpatterns = [
    path('', views.AddUrlView.as_view(), name='add_url'),
    path('list/', views.UrlListView.as_view(), name='url_list'),
    path('<str:short_url>/', views.RedirectShortUrlView.as_view(), name='redirect_short_url'),
]