from django.urls import path

from .views import merch_list, index

urlpatterns = [
    path('', index, name='index'),
    path('merchstore/items', merch_list, name = "merchstore-items"),
]

app_name = "merchstore"