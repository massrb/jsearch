from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.utils.http import urlencode
from jobsearch.models import JobSearch, LocationSearch, JobListing
from .forms import SelectTypeForm, JobSearchForm

# Create your views here.
from django.http import HttpResponse

def index(request):
  search_type = request.GET.get('js', '').lower()
  select_type = request.GET.get('filter', '').lower()
  exclude = request.GET.get('e', '0')
  if request.method == 'POST':
    js_form = JobSearchForm(request.POST)
    filt_type = SelectTypeForm(request.POST)
    if js_form.is_valid() and filt_type.is_valid():    
      fld = js_form.cleaned_data # ['id_searches']
      ftyp = filt_type.cleaned_data
      redirect_url = reverse('index')
      parameters = urlencode({'js': ','.join(fld['searches']), 'filter': ftyp['selection_type']})
      return redirect(f'{redirect_url}?{parameters}')
    else:
      for field in js_form:
        print(f"Field Error for field {field.name}:  {field.errors}")
      return render(request, "index.html", {'form':js_form})
  else:
    rec_ids = [] if search_type in [None,''] else [int(numeric_string) for numeric_string in search_type.split(',')]
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

    select_form = SelectTypeForm(initial={'selection_type': select_type})
    jobsearch_form = JobSearchForm(initial={'searches': search_type.split(',')})
    return render(request, "index.html", {'jobs': jobs, 'select_type': select_form, 'jobsearch': jobsearch_form})