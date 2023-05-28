from django.db import models
from . import services

# Create your models here.

class Project(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_projects():
        project_results = services.Api.get_api_json("/rest/v2/projects")
        projects = []

        for project_result in project_results:
            projects.append(Project(project_result.id, project_result.name))

        return projects
    
    def get_project(name):
        projects = Project.get_projects()
        project = [project for project in projects if project.name == name]
        
        return project[0]
    
class Task:

    def create_tasks(tasks):
        project = Project.get_project("Inbox")

        for task in tasks:
            Task.create_task(task, project.id)

    def create_task(name, project_id):
        request_body = {
            "content": name,
            "project_id": project_id
        }

        services.Api.post_api_json("/rest/v2/tasks", request_body)