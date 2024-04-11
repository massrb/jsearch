from django.contrib import admin

from .models import JobSearch, LocationSearch

# Register your models here.

@admin.register(JobSearch)
class JobSearchAdmin(admin.ModelAdmin):
  pass

@admin.register(LocationSearch)
class LocationSearchAdmin(admin.ModelAdmin):
  pass
