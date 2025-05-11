from django.urls import path
from .views import CommissionListView, CommissionDetailView, CreateCommissionView, CommissionUpdateView, JobView

urlpatterns = [
	path('list', CommissionListView.as_view(), name='commissionList'),
	path('detail/<int:pk>', CommissionDetailView.as_view(), 
    	name='commissionDetail'),
	path('add', CreateCommissionView.as_view(), 
    	name='commissionAdd'),
	path('detail/<int:pk>/edit', CommissionUpdateView.as_view(), 
    	name='commissionEdit'),
	path('jobDetail/<int:pk>', JobView.as_view(), 
    	name='jobDetail'),
]

app_name = "commissions"

