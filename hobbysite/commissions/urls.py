from django.urls import path
from .views import CommissionListView, CommissionDetailView

urlpatterns = [
	path('list', CommissionListView.as_view(), name='commissionList'),
	path('detail/<int:pk>', CommissionDetailView.as_view(), 
    	name='commissionDetail'),
]

app_name = "commissions"

