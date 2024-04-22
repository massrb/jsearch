from django.core.management.base import BaseCommand, CommandError
from jobsearch.models import JobListing

class Command(BaseCommand):
  help = 'Cleanup jobs'

  def add_arguments(self, parser):
    parser.add_argument('-a', '--add', nargs='?', const='1', help='add keys to job listings')
    parser.add_argument('-c', '--clean', nargs='?', const='1', help='Clean up job listings')


  def handle(self, *args, **options):
    if options['add']: 
      count = 0
      info_count = 0
      for job in JobListing.objects.all():
        if job.jkey == '':
          count += 1
          job.set_jkey()
        elif info_count < 30:
          info_count += 1
          print(job)
          print('*******************************')
      print(f'{count} out of {len(JobListing.objects.all())} had no jkey')

    elif options['clean']:
      count = 0
      map = {}
      for job in JobListing.objects.all():
        if job.jkey in map and job.jkey != '':
          count += 1
          job.delete()
        else:
          map[job.jkey] = True
      print(f'{count} duplicates seen')        
