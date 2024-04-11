from django.shortcuts import render
from jobsearch.models import JobSearch, LocationSearch, JobListing

# Create your views here.
from django.http import HttpResponse

def index(request):
  return render(request, "index.html", {'jobs': JobListing.objects.all()})