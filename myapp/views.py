from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from myapp.models import Project, Task
from .forms import CreateNewTask, CreateNewProject


# Create your views here.
def index(request):
    title = 'Hello, Django!'
    return render(request, 'index.html', {
        'title': title
    })


def about(request):
    username = 'Yussef'
    return render(request, 'about.html', {
        'username': username})


def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects/projects.html', {
        'projects': projects
    })


def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/tasks.html', {
        'tasks': tasks
    })


def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks/create_task.html', {
            'form': CreateNewTask()
        })
    else:
        Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            project_id=2,
        )
        return redirect('tasks')


def create_project(request):
    if request.method == 'GET':
        return render(request, 'projects/create_project.html', {
            'form': CreateNewProject()
        })
    else:
        Project.objects.create(
            name=request.POST['name'],
        )
        return redirect('projects')


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project_id=project_id)
    return render(request, 'projects/project_detail.html',{
        'project': project,
        'tasks': tasks
    })
