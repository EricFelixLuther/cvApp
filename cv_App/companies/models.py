from django.db import models
from simple_history.models import HistoricalRecords


class CompanyType(models.Model):
    name = models.CharField(max_length=64)


class Company(models.Model):
    name = models.CharField(max_length=64)
    company_type = models.ForeignKey(CompanyType, on_delete=models.CASCADE, blank=True, null=True)
    location = models.CharField(max_length=128, blank=True)  # TODO: geolocation
    notes = models.TextField(blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class ContactPerson(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    role = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=64, blank=True)
    email = models.EmailField(max_length=128, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    linkedin = models.URLField(max_length=256, blank=True)
    notes = models.TextField(blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('last_name', 'first_name')
