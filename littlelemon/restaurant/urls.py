# define URL route for index() view
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = 'restaurant'
urlpatterns = [
    path('', views.index, name='index'),
    path('api-token-auth/', obtain_auth_token),
    path('menu/', views.MenuItemView.as_view(), name="menu-list"),
    path('menu/<int:pk>', views.SingleMenuItemView.as_view(), name="menu-detail"),
]
