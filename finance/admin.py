from django.contrib import admin
from .models import FinancialRecord

@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'date', 'revenue', 'expenses', 'profit')
    list_filter = ('company_name', 'date')
    search_fields = ('company_name',)

admin.site.site_header = "Управление Финансами"
admin.site.index_title = "Администрирование данных"
