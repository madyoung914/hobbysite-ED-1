from django.urls import path
from .views import (CommissionListView, CommissionDetailView,
                    CreateCommissionView, CommissionUpdateView, JobView)

urlpatterns = [
    path('list', CommissionListView.as_view(), name='commissions-list'),
    path('detail/<int:pk>', CommissionDetailView.as_view(),
         name='commission-detail'),
    path('add', CreateCommissionView.as_view(),
         name='commission-add'),
    path('<int:pk>/edit', CommissionUpdateView.as_view(),
         name='commission-edit'),
    path('job/<int:pk>', JobView.as_view(),
         name='job-detail'),
]

app_name = "commissions"
