from django.urls import path
from . import views

urlpatterns = [
    path('get_constats/', views.get_constats, name='get_constats'),
    path('create-constat/', views.create_constat, name='create_constat'),
    path('update-constat/<int:constat_id>/', views.update_constat_with_codeb, name='update_constat_with_codeb'),
    path('update-constat-file/<str:constat_id>/<str:type>/<str:cin>/', views.update_constat_with_file, name='update_constat_with_file'),
]
