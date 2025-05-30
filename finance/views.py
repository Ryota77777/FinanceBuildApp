from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Project, WorkStage, WorkType, Cost, Purchase, Material
from .forms import RegisterForm, ProjectForm, WorkStageForm, WorkTypeForm, CostForm, PurchaseForm, MaterialForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, F, ExpressionWrapper, DecimalField


def home(request):
    return render(request, 'home.html')


# ---------- Аутентификация ----------

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация успешна!")
            return redirect('home')
        else:
            messages.error(request, "Ошибка при регистрации.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    # Очистка старых сообщений перед авторизацией
    storage = messages.get_messages(request)
    storage.used = True

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('home')
        messages.error(request, "Неверный логин или пароль.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


# ---------- Обзор проектов ----------

@login_required
def project_list(request):
    projects = Project.objects.filter(author=request.user)
    return render(request, 'projects/list.html', {'projects': projects})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, author=request.user)
    stages = project.stages.all()
    costs = project.costs.all()
    purchases = project.purchases.all()
    return render(request, 'projects/detail.html', {
        'project': project,
        'stages': stages,
        'costs': costs,
        'purchases': purchases,
    })


@login_required
def workstage_detail(request, pk):
    stage = get_object_or_404(WorkStage, pk=pk)
    work_types = stage.work_types.all()
    return render(request, 'projects/stage_detail.html', {
        'stage': stage,
        'work_types': work_types,
    })


@login_required
def worktype_detail(request, pk):
    worktype = get_object_or_404(WorkType, pk=pk)
    return render(request, 'projects/worktype_detail.html', {'worktype': worktype})


# ---------- Планирование ----------

@login_required
def planning_page(request):
    return render(request, 'planning/planning_page.html')


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            return redirect('planning_page')
    else:
        form = ProjectForm()
    return render(request, 'planning/project_form.html', {'form': form})


@login_required
def workstage_create(request):
    if request.method == 'POST':
        form = WorkStageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('planning_page')
    else:
        form = WorkStageForm()
    return render(request, 'planning/workstage_form.html', {'form': form})


@login_required
def worktype_create(request):
    if request.method == 'POST':
        form = WorkTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('planning_page')
    else:
        form = WorkTypeForm()
    return render(request, 'planning/worktype_form.html', {'form': form})


@login_required
def cost_create(request):
    if request.method == 'POST':
        form = CostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('planning_page')
    else:
        form = CostForm()
    return render(request, 'planning/cost_form.html', {'form': form})


@login_required
def purchase_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save()
            material = purchase.material
            material.stock += purchase.quantity
            material.save()
            return redirect('planning_paget')
    else:
        form = PurchaseForm()
    return render(request, 'planning/purchase_form.html', {'form': form})

@login_required
def material_create(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('planning_page')  
    else:
        form = MaterialForm()
    return render(request, 'planning/material_form.html', {'form': form})


# ---------- Расчёт закупок ----------

@login_required
def purchase_calculation_page(request):
    projects = Project.objects.filter(author=request.user)
    return render(request, 'purchase_calculation/purchase_calculation_page.html', {
        'projects': projects
    })

@login_required
def material_needs(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    work_types = WorkType.objects.filter(stage__project=project)
    material_data = {}

    for wt in work_types:
        if wt.material not in material_data:
            material_data[wt.material] = {'needed': 0, 'purchased': 0}
        material_data[wt.material]['needed'] += wt.total_material_needed()

    purchases = Purchase.objects.filter(project=project)
    for p in purchases:
        if p.material in material_data:
            material_data[p.material]['purchased'] += p.quantity
    
    for material, data in material_data.items():
        data['remaining'] = round(data['needed'] - data['purchased'], 2)

    return render(request, 'purchase_calculation/material_needs.html', {
        'project': project,
        'material_data': material_data
    })

@login_required
def purchase_summary(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    purchases = Purchase.objects.filter(project=project)
    return render(request, 'purchase_calculation/purchase_summary.html', {
        'project': project,
        'purchases': purchases
    })

# ---------- Оптимизация ----------

@login_required
def optimization_page(request):
    projects = Project.objects.filter(author=request.user)
    return render(request, 'optimization/optimization_page.html', {'projects': projects})

@login_required
def optimization_summary(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    work_types = WorkType.objects.filter(stage__project=project)
    total_labor = sum([wt.total_labor_cost() for wt in work_types])
    total_material = sum([wt.total_material_needed() * wt.material.price_per_unit for wt in work_types])
    return render(request, 'optimization/summary.html', {
        'project': project,
        'total_labor': total_labor,
        'total_material': total_material,
    })


@login_required
def optimization_recommendations(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    recommendations = []
    for material in Material.objects.all():
        if material.stock > 100:
            recommendations.append(f"Материала '{material.name}' в избытке — {material.stock} {material.unit}.")
    return render(request, 'optimization/recommendations.html', {
        'project': project,
        'recommendations': recommendations
    })


# ---------- Профиль ----------

@login_required
def profile(request):
    return render(request, 'profile/profile.html', {'user': request.user})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Профиль обновлён')
        return redirect('profile')
    return render(request, 'profile/profile_edit.html', {'user': request.user})


