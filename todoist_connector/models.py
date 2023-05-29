from django.db import models
from . import services

# Create your models here.


class Project(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_projects(todoist_api_key):
        project_results = services.Api.get_api_json("/rest/v2/projects", todoist_api_key)
        projects = []

        for project_result in project_results:
            projects.append(Project(project_result.id, project_result.name))

        return projects

    def get_project(name, todoist_api_key):
        projects = Project.get_projects(todoist_api_key)
        project = [project for project in projects if project.name == name]

        return project[0]


class Task:

    def create_tasks(tasks, todoist_api_key):
        project = Project.get_project("Inbox", todoist_api_key)

        for task in tasks:
            Task.create_task(task, project.id, todoist_api_key)

        return project

    def create_task(name, project_id, todoist_api_key):
        request_body = {
            "content": name,
            "project_id": project_id
        }

        services.Api.post_api_json("/rest/v2/tasks", request_body, todoist_api_key)
