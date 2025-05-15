from django.urls import path
from .views import ProductCreateView, ProductTypeListView, ProductDetailView
from .views import ProductUpdateView, CartView, TransactionListView

urlpatterns = [
    path('items', ProductTypeListView.as_view(), name="merchstore-list"),
    path('item/<int:pk>', ProductDetailView.as_view(),
         name="merchstore-item"),
    path('item/add', ProductCreateView.as_view(), name="merch-add"),
    path('item/<int:pk>/edit', ProductUpdateView.as_view(), name="merch-edit"),
    path('cart', CartView.as_view(), name="merch-cart"),
    path('transactions', TransactionListView.as_view(),
         name="merch-transactions"),
]

app_name = "merchstore"
