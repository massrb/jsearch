from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.utils.http import urlencode
from jobsearch.models import JobSearch, LocationSearch, JobListing
from .forms import SelectTypeForm, JobSearchForm, LocationSearchForm, LocationTypeForm

# Create your views here.
from django.http import HttpResponse

def index(request):
  search_type = request.GET.get('js', '').lower()
  select_type = request.GET.get('filter', '').lower()
  loc = request.GET.get('loc', '').lower()
  loc_type = request.GET.get('ltyp', '').lower()

  if request.method == 'POST':
    js_form = JobSearchForm(request.POST)
    filt_type = SelectTypeForm(request.POST)
    loc_form = LocationSearchForm(request.POST)
    ltype_form = LocationTypeForm(request.POST)
    if js_form.is_valid() and filt_type.is_valid() and loc_form.is_valid() and ltype_form.is_valid():
      fld = js_form.cleaned_data # ['id_searches']
      ftyp = filt_type.cleaned_data
      locfld = loc_form.cleaned_data
      ltype = ltype_form.cleaned_data
      redirect_url = reverse('index')
      parameters = urlencode({'js': ','.join(fld['searches']),
                             'filter': ftyp['selection_type'],
                             'loc': ','.join(locfld['location']),
                             'ltyp': ltype['location_type']})

      return redirect(f'{redirect_url}?{parameters}')
    else:
      for field in js_form:
        print(f"Field Error for field {field.name}:  {field.errors}")
      for field in filt_type:
        print(f"Filter Field Error for field {field.name}:  {field.errors}")
      return render(request, "index.html", {'form':js_form})
  else:
    print('stype', search_type)
    rec_ids = [] if search_type in [None,''] else [int(numeric_string) for numeric_string in search_type.split(',')]
    if len(rec_ids) != 0:
      js = JobSearch.objects.filter(id__in=rec_ids)

    loc_ids = [] if loc in [None,''] else [int(numeric_string) for numeric_string in loc.split(',')]
    if (len(loc_ids)) != 0:
      loc_recs = LocationSearch.objects.filter(id__in=loc_ids)
    jobs = JobListing.objects.all()
    if 'js' in locals() and js.exists():
      if select_type == 'inc':
        jobs = jobs.filter(job_search__in=js)
      else:
        jobs = jobs.exclude(job_search__in=js)

    if 'loc_recs' in locals() and loc_recs.exists():
      if loc_type == 'inc':
        jobs = jobs.filter(search_location__in=loc_recs)
      else:
        jobs = jobs.exclude(search_location__in=loc_recs)

    print(f'{len(jobs)} jobs')

    select_form = SelectTypeForm(initial={'selection_type': select_type})
    jobsearch_form = JobSearchForm(initial={'searches': search_type.split(',')})
    location_form = LocationSearchForm(initial={'location': loc.split(',')})
    loctype_form = LocationTypeForm(initial={'location_type': loc_type})

    return render(request, "index.html", {'jobs': jobs, 'select_type': select_form,
                                          'jobsearch': jobsearch_form,
                                          'loc_search': location_form,
                                          'loc_type': loctype_form})