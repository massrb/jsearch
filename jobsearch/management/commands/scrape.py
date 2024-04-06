from django.core.management.base import BaseCommand, CommandError
from jobsearch.models import JobSearch, LocationSearch, JobListing
from .skyscrape import IndeedScraper
from .indeed_job import IndeedJob 

class Command(BaseCommand):

  help = 'Description of my custom Scrape command'

  def handle(self, *args, **options):
    # Code for your custom command goes here
    self.stdout.write('My custom scrape command executed successfully')
    list = JobSearch.objects.all()
    if (len(list) > 0):
      self.stdout.write(f'list: {list} {list[0].search_string}')
    scraper = IndeedScraper('Ruby+Developer', 'Boston')
    print('after ctor')
    scraper.accumulate()
    js_q = JobSearch.objects.filter(search_string='Ruby')
    loc_q = LocationSearch.objects.filter(location="Boston")
    js_location = loc_q[0] if len(loc_q) > 0 else LocationSearch(location="Boston", local_search=True)
    jb_search = js_q[0] if len(js_q) > 0 else JobSearch(search_string='Ruby')
    if jb_search._state.adding: jb_search.save()
    if js_location._state.adding: js_location.save()
      
    for idx, job in enumerate(scraper.jobs):
      if idx == 0:
        job_link = job.fld_val('job_link')
        job_title = job.fld_val('job_title')
        company = job.fld_val('company')
        company_location = job.fld_val('company_location')

        job_type = job.fld_val('job_type')
        apply_type = job.fld_val('apply')
        job_listing = JobListing(job_link=job_link, job_title=job_title, company=company,
                                 company_location=company_location, job_type=job_type,
                                 apply_type=apply_type, job_search=jb_search, 
                                 search_location=js_location)
        job_listing.save()

      print(job)
      print("\n\n" + "*" * 30 + "\n\n")

    print(f"{len(scraper.jobs)} jobs")
    print(scraper)