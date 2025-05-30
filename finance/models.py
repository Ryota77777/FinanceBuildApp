from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class WorkStage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.project.name} — {self.name}"

class Material(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class WorkType(models.Model):
    stage = models.ForeignKey(WorkStage, on_delete=models.CASCADE, related_name='work_types')
    name = models.CharField(max_length=200)
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    material_needed_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    labor_cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def total_material_needed(self):
        return self.volume * self.material_needed_per_unit

    def total_labor_cost(self):
        return self.volume * self.labor_cost_per_unit

class Cost(models.Model):
    COST_TYPES = [
        ('материалы', 'Материалы'),
        ('труд', 'Труд'),
        ('техника', 'Техника'),
        ('прочее', 'Прочее'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='costs')
    description = models.CharField(max_length=200)
    cost_type = models.CharField(max_length=50, choices=COST_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.project.name}: {self.description}"

class Purchase(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='purchases')

    def __str__(self):
        return f"Закупка: {self.material.name} — {self.quantity} ({self.project.name})"

