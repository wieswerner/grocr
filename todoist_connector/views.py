from django.shortcuts import render

# Create your views here.
def sync(request):
    return render(request, "sync.html")