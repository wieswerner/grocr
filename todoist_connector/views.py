from django.shortcuts import render
from . import models
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# adding exempt as a workaround for
@csrf_exempt
def sync(request):
    todoist_api_key = request.COOKIES['Todoist_Api_Key']
    tasks = []

    for key in [key for key in request.POST if not key == "csrfmiddlewaretoken"]:
        tasks.append(request.POST[key])

    project = models.Task.create_tasks(tasks, todoist_api_key)
    return render(request, "sync.html", {"count": len(tasks), "project_id": project.id, "project_name": project.name})
