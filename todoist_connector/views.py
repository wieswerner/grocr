from django.shortcuts import render
from . import models

# Create your views here.
def sync(request):
    tasks = []

    for key in [key for key in request.POST if not key == "csrfmiddlewaretoken"]:
        tasks.append(request.POST[key])

    models.Task.create_tasks(tasks)
    return render(request, "sync.html")