from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from .models import AgencyRequest
from .forms import AgencyRequestForm
from django.urls import reverse_lazy
class AgencyCreate(CreateView):
    # model=AgencyRequest
    template_name = 'agency_request_form/agency_request_form.html'
    # template_name = 'agency_request_form/test.html'
    # fields = '__all__'

    form_class = AgencyRequestForm
    success_url = reverse_lazy("agency_request_list") #reverse_lazy takes the name in the urlconf and maps it
    #to the equivalent path
    #In function based views -> use return redirect("name_of_the_url_conf")

    

    

