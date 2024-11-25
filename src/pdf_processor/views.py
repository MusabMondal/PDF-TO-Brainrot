from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

def home(request):
    return render(request, 'home.html')

class MainPageView(TemplateView):
    template_name = "home.html"