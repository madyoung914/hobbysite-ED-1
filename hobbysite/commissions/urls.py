from django.urls import path
from .views import CommissionListView, CommissionDetailView, CreateCommissionView, CommissionUpdateView

urlpatterns = [
	path('list', CommissionListView.as_view(), name='commissionList'),
	path('detail/<int:pk>', CommissionDetailView.as_view(), 
    	name='commissionDetail'),
	path('add', CreateCommissionView.as_view(), 
    	name='commissionAdd'),
	path('detail/<int:pk>/edit', CommissionUpdateView.as_view(), 
    	name='commissionEdit'),
]

app_name = "commissions"

