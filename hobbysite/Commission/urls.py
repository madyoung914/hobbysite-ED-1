from django.urls import path
from .views import 
urlpatterns = [
	path('commission/list', commissionListView, name='commissionList'),
	path('commission/detail/<int:pk>', commissionDetailView, name='commissionDetail'),
]
app_name = "Commission"