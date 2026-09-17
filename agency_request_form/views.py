from django.shortcuts import render, get_object_or_404,redirect
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

def update_request(request,pk):

    agency_values = get_object_or_404(AgencyRequest, pk = pk)

    if request.method == 'POST':
        #This is when the user is submitting the updated form
        form = AgencyRequestForm(request.POST,instance=agency_values) #Here request.POST has the new values
        #instance = agency_values has the old values to be updated

        if form.is_valid():
            form.save()
            return redirect("agency_request_list")
    else:
        #This is when the user just visited the update form after clicking it
        #So we make display the form with the values of pk = pk

        form = AgencyRequestForm(instance=agency_values)

        return render(request,
                      "agency_request_form/agency_request_form.html",
                      {"form" : form})
    

def delete_request(request,pk):
    agency_values = get_object_or_404(AgencyRequest,pk=pk)

    agency_values.delete()

    return redirect("agency_request_list")

