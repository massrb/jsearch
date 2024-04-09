from django.core.management.base import BaseCommand, CommandError
from jobsearch.models import JobSearch, LocationSearch, JobListing
from .skyscrape import IndeedScraper
from .indeed_job import IndeedJob
import re

PATTERN = (r'\bmobile\b|\bjava\b|\bc#|.net\b|\bc\+\+|'
           r'\bndroid\b|\bvue\bvuejs\b|\bangular\b|'
           r'\bsite\s+reliability\b|\bmulesoft\b|\blead\b|'
           r'\bwordpress\b'
           )

RGPAT = re.compile(PATTERN, re.IGNORECASE)

class Command(BaseCommand):

  help = 'Description of my custom Scrape command'

  def add_arguments(self, parser):
    parser.add_argument('-p', '--jobs', type=int, help='number of jobs to save to DB')


  def save_jobs(self, scraper, count):
    
    save_count = 0
    for idx, job in enumerate(scraper.jobs):
      job_title = job.fld_val('job_title')
      if RGPAT.search(job_title):
        print(f'SKIP: {job_title}\n\n')
        continue

      if save_count < count:
        job_link = job.fld_val('job_link')
        

        job_rec = JobListing.objects.filter(job_link=job_link)
        if len(job_rec) > 0: next

        company = job.fld_val('company')
        company_location = job.fld_val('company_location')

        job_type = job.fld_val('job_type')
        apply_type = job.fld_val('apply')
        job_listing = JobListing(job_link=job_link, job_title=job_title, company=company,
                                 company_location=company_location, job_type=job_type,
                                 apply_type=apply_type, job_search=jb_search, 
                                 search_location=js_location)
        job_listing.save()
        save_count += 1
        
      print(job)
      print("\n\n" + "*" * 30 + "\n\n")

    print(f"{len(scraper.jobs)} jobs")
    print(scraper)


  def handle(self, *args, **options):
    # Code for your custom command goes here
    self.stdout.write('web scrape utility ..')
    job_count = options['jobs']
    
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
    self.save_jobs(scraper, job_count)
      
    