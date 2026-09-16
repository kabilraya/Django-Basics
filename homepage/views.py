from django.shortcuts import render
from agency_request_form.models import AgencyRequest
from django.views.generic import ListView

class ListAgencyRequest(ListView):
    model = AgencyRequest
    template_name = "home/index.html"
    context_object_name = "agencies_object"
    