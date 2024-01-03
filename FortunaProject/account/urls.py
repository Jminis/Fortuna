from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('create/', views.create_team_view, name='create_team'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/<int:team_id>/', views.delete_team_view, name='delete_team'),

]