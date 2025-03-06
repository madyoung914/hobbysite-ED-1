from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Commission

class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/CommissionList.html' 


class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/CommissionDetail.html' 
# Create your views here.
