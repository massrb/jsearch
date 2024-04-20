from django.contrib import admin

from .models import JobSearch, LocationSearch, JobListing

# Register your models here.

@admin.register(JobSearch)
class JobSearchAdmin(admin.ModelAdmin):
  list_display = ("search_string", "active")

@admin.register(LocationSearch)
class LocationSearchAdmin(admin.ModelAdmin):
  list_display = ("location", "local_search", "active")

@admin.register(JobListing)
class JobListingSearchAdmin(admin.ModelAdmin):
  list_display = ("job_title", "company", "last_seen", "update_time")
