from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/users/', views.admin_users, name='admin_users'),
    path('admin-dashboard/properties/', views.admin_properties, name='admin_properties'),
    path('admin-dashboard/properties/new/', views.admin_property_form, name='admin_property_new'),
    path('admin-dashboard/properties/<int:pk>/edit/', views.admin_property_form, name='admin_property_edit'),
    path('admin-dashboard/properties/<int:pk>/delete/', views.admin_property_delete, name='admin_property_delete'),
    path('propriedades/<int:pk>/', views.property_detail, name='property_detail'),
]
