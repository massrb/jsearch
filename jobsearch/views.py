from django.shortcuts import render
from jobsearch.models import JobSearch, LocationSearch, JobListing

# Create your views here.
from django.http import HttpResponse

def index(request):
  search_type = request.GET.get('t', '').lower()
  exclude = request.GET.get('e', '0')
  
  if search_type == 'ruby':
    js = JobSearch.objects.filter(search_string='Ruby')
  elif search_type == 'python':
    js = JobSearch.objects.filter(search_string='Python')
  else:
    jobs = JobListing.objects.all()

  if not 'jobs' in locals():
    all = JobListing.objects.all()
    if exclude == '1':
      jobs = all if not js.exists() else all.exclude(job_search=js.first())
    else:
      jobs = JobListing.objects.filter(job_search=js.first())
  return render(request, "index.html", {'jobs': jobs})