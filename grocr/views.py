from django.shortcuts import render
from . import views
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# adding exempt as a workaround for testing
@csrf_exempt
def home(request):
    return render(request, "home.html")
