from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Project
from .forms import ProjectForm


def can_manage(user, project):
    """Роботу редагує та видаляє її автор; модератори й адміністратори — будь-яку."""
    return user == project.author or user.is_superuser or user.role in ('admin', 'moderator')

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'portfolio/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'portfolio/project_detail.html', {
        'project': project,
        'can_manage': request.user.is_authenticated and can_manage(request.user, project),
    })

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            return redirect('portfolio:project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'portfolio/project_form.html', {'form': form})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not can_manage(request.user, project):
        raise PermissionDenied
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('portfolio:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'portfolio/project_form.html', {'form': form, 'project': project})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not can_manage(request.user, project):
        raise PermissionDenied
    if request.method == 'POST':
        project.delete()
        return redirect('portfolio:project_list')
    return render(request, 'portfolio/project_confirm_delete.html', {'project': project})
