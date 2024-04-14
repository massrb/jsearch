from django.core.management.base import BaseCommand, CommandError
from jobsearch.models import JobSearch, LocationSearch, JobListing
from .skyscrape import IndeedScraper
from .indeed_job import IndeedJob
import re
import time

PATTERN = (r'\bmobile\b|\bjava\b|\bc#|.net\b|\bc\+\+|'
           r'\bndroid\b|\bvue\bvuejs\b|\bangular\b|'
           r'\bsite\s+reliability\b|\bmulesoft\b|\blead\b|'
           r'\bwordpress\b|\bmanager\b|\bdevops\b|\bcoach\b|'
           r'\bcustomer\s+support\s+representative\b'
           )

RGPAT = re.compile(PATTERN, re.IGNORECASE)

class Command(BaseCommand):

  help = 'Description of my custom Scrape command'

  def add_arguments(self, parser):
    parser.add_argument('-j', '--jobs', type=int, help='number of jobs to save to DB')
    # parser.add_argument('-l', '--local-html', nargs='?', type=str, default='doc.html', help='use local html doc')
    parser.add_argument('-s', '--search', nargs='?', type=str, help='search string')
    parser.add_argument('-l', '--loc', nargs='?', type=str, help='location for search')



  def save_jobs(self, scraper, count):
    
    save_count = 0
    for idx, job in enumerate(scraper.jobs):
      job_title = job.fld_val('job_title')
      if not self.location.local_search and re.search(r'\bremote\b', job_title) == None:
        continue
      if RGPAT.search(job_title):
        print(f'SKIP: {job_title}\n\n')
        continue

      if save_count < count:
        job_link = job.fld_val('job_link')        

        job_rec = JobListing.objects.filter(job_link=job_link)
        if len(job_rec) > 0: continue

        company = job.fld_val('company')
        company_location = job.fld_val('company_location')

        job_type = job.fld_val('job_type')
        apply_type = job.fld_val('apply')
        job_listing = JobListing(job_link=job_link, job_title=job_title, company=company,
                                 company_location=company_location, job_type=job_type,
                                 apply_type=apply_type, job_search=self.job_search, 
                                 search_location=self.location)
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
    search = options['search']
    location = options['loc']
    job_count = 120 if job_count == None else job_count

    list = JobSearch.objects.all()
    if (len(list) > 0):
      self.stdout.write(f'list: {list} {list[0].search_string}')
    
    if search == None:
      js_q = JobSearch.objects.filter(active=True)
    else: 
      js_q = JobSearch.objects.filter(active=True, search_string=search)

    if location == None:
      loc_q = LocationSearch.objects.filter(active=True)
    else: 
      loc_q = LocationSearch.objects.filter(active=True, location=location)
    for js in js_q:
      for jloc in loc_q:
        self.job_search = js
        self.location = jloc
        scraper = IndeedScraper(js.search_string, jloc.location, options)
        scraper.accumulate()
        self.save_jobs(scraper, job_count)
        time.sleep(5)
      
    