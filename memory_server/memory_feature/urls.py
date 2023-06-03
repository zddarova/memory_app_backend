from django.urls import path
from .views import memory_list_create, memory_retrieve_update_destroy

urlpatterns = [
    path('memories/', memory_list_create, name='memory_list_create'),
    path('memories/<int:pk>/', memory_retrieve_update_destroy, name='memory_retrieve_update_destroy'),
]
