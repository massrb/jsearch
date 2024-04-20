from django import forms
from jobsearch.models import JobSearch, LocationSearch

class JobSearchForm(forms.Form):
  recs = JobSearch.objects.filter(active=True)
  choices = map(lambda r: [str(r.id), r.search_string], recs)
  searches = forms.MultipleChoiceField(
    widget=forms.SelectMultiple,
    choices=choices,
  )
  def clean(self):
 
    # data from the form is fetched using super function
    super(JobSearchForm, self).clean()
    return self.cleaned_data

class SelectTypeForm(forms.Form):
  OPTIONS = (
    ("inc", "Include"),
    ("exc", "Exclude"),
  )
  selection_type = forms.ChoiceField(widget=forms.RadioSelect,
                                          choices=OPTIONS)

class LocationSearchForm(forms.Form):
  recs = LocationSearch.objects.filter(active=True)
  choices = map(lambda r: [str(r.id), r.location], recs)
  location = forms.MultipleChoiceField(
    widget=forms.SelectMultiple,
    choices=choices,
  )
  def clean(self):

    # data from the form is fetched using super function
    super(LocationSearchForm, self).clean()
    return self.cleaned_data

class LocationTypeForm(forms.Form):
  OPTIONS = (
    ("inc", "Include"),
    ("exc", "Exclude"),
  )
  location_type = forms.ChoiceField(widget=forms.RadioSelect,
                                          choices=OPTIONS)
