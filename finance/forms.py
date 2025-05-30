from django import forms
from .models import Project, WorkStage, Material, WorkType, Cost, Purchase, User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date'] 
        labels = {
            'name': 'Название проекта',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
            'description': 'Описание',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class WorkStageForm(forms.ModelForm):
    class Meta:
        model = WorkStage
        fields = ['project', 'name', 'description']
        labels = {
            'project': 'Проект',
            'name': 'Название этапа',
            'description': 'Описание',
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'unit', 'price_per_unit', 'stock']
        labels = {
            'name': 'Название',
            'unit': 'Единица измерения',
            'price_per_unit': 'Цена за единицу',
            'stock': 'Остаток на складе',
        }

class WorkTypeForm(forms.ModelForm):
    class Meta:
        model = WorkType
        fields = ['stage', 'name', 'volume', 'unit', 'material', 'material_needed_per_unit', 'labor_cost_per_unit']
        labels = {
            'stage': 'Этап',
            'name': 'Название работы',
            'volume': 'Объем',
            'unit': 'Единица измерения',
            'material': 'Материал',
            'material_needed_per_unit': 'Материала на единицу',
            'labor_cost_per_unit': 'Трудозатраты на единицу',
        }

class CostForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['project', 'description', 'cost_type', 'amount', 'date']
        labels = {
            'project': 'Проект',
            'description': 'Описание',
            'cost_type': 'Тип затрат',
            'amount': 'Сумма',
            'date': 'Дата',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['project', 'material', 'quantity', 'date']
        labels = {
            'project': 'Проект',
            'material': 'Материал',
            'quantity': 'Количество',
            'date': 'Дата',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
