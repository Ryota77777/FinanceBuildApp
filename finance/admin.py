from django.contrib import admin
from .models import Project, WorkStage, Material, WorkType, Cost, Purchase

admin.site.register(Project)
admin.site.register(WorkStage)
admin.site.register(Material)
admin.site.register(WorkType)
admin.site.register(Cost)
admin.site.register(Purchase)
