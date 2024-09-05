from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),

    path('admin/', views.AdminTemplate.as_view(), name='admin_statistics'),
    path('admin/create-user/', views.AdminUserCreateView.as_view(), name='create_user'),
    path('admin/delete-url/<int:pk>/', views.DeleteUrlView.as_view(), name='delete_url'),
    path('admin/delete-user/<int:pk>/', views.DeleteUserView.as_view(), name='delete_user'),
]
