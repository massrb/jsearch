import datetime
from django.utils import timezone
from django.db import models

# Create your models here.

class JobSearch(models.Model):
  search_string = models.CharField(max_length=120)
  platform = models.CharField(max_length=50, default='Indeed')
  active = models.BooleanField(default=True)

class LocationSearch(models.Model):
  location = models.CharField(max_length=50)
  platform = models.CharField(max_length=50)
  local_search = models.BooleanField(default=False)
  active = models.BooleanField(default=True)

class JobListing(models.Model):
  job_link = models.CharField(max_length=350)
  job_title = models.CharField(max_length=120)
  last_seen = models.DateTimeField(auto_now_add=True, blank=True)
  company = models.CharField(max_length=100)
  company_location = models.CharField(max_length=100)
  # can be full time or salary
  job_type = models.CharField(max_length=100)
  # easy apply etc
  apply_type = models.CharField(max_length=35)
  create_time = models.DateTimeField(auto_now_add=True)
  update_time = models.DateTimeField(auto_now=True)
  job_search = models.ForeignKey(JobSearch, on_delete=models.CASCADE)
  search_location = models.ForeignKey(LocationSearch, on_delete=models.CASCADE)


