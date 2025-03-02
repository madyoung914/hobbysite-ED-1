from django.urls import path
from .views import CommissionListView, CommissionDetailView

urlpatterns = [
	path('commission/list', CommissionListView.as_view(), name='commissionList'),
	path('commission/detail/<int:pk>', CommissionDetailView.as_view(), name='commissionDetail'),
]
app_name = "Commission"