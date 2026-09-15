from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from .models import AgencyRequest
from .forms import AgencyRequestForm

class AgencyCreate(CreateView):
    # model=AgencyRequest
    template_name = 'agency_request_form/agency_request_form.html'
    # template_name = 'agency_request_form/test.html'
    # fields = '__all__'

    form_class = AgencyRequestForm

    def form_valid(self, form):
        return super().form_valid(form)

    

