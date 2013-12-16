from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
#from django.views.generic.simple import direct_to_template

from models import Client

# Create your views here.
def index(request):
    return HttpResponse("Ola kala!")

class ClientsListView(ListView):
    model = Client

def show_clients(request):
    return direct_to_template(request, template='clients.html',
                              extra_context={'clients':Client.objects.get_all()})
