from django.db import models

class FinancialRecord(models.Model):
    company_name = models.CharField(max_length=255)
    date = models.DateField()
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    expenses = models.DecimalField(max_digits=15, decimal_places=2)
    profit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.profit = self.revenue - self.expenses
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company_name} ({self.date})"
