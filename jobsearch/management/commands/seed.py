
from django.core.management.base import BaseCommand
from jobsearch.models import JobSearch, LocationSearch
import random
import logging
logger = logging.getLogger(__name__)

# python manage.py seed --mode=refresh

""" Clear all data and creates records """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
      parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
      self.stdout.write('seeding data...')
      self.run_seed(options['mode'])
      self.stdout.write('done.')


    def clear_data(self):
      """Deletes all the table data"""
      logger.info("Delete Location and JobSearch instances")
      LocationSearch.objects.all().delete()
      JobSearch.objects.all().delete()


    def create_data(self):
      """Creates an address object combining different elements from the list"""
      logger.info("Creating location and job search data")

      loc = LocationSearch(location='Boston', local_search=True)
      loc.save()

      loc2 = LocationSearch(location='Worcester', local_search=True)
      loc2.save()

      locations = ['Nashua+NH', 'DC', 'NYC', 'Hartford+CT', 'Portland+Maine', 'Burlington+VT', 'Albany+NY', 'Chicago',
                   'Minneapolis', 'Detroit', 'Miami', 'Denver', 'Houston', 'Dallas']
      skills = ['Ruby', 'Javascript', 'React']

      for area in locations:
        place = LocationSearch(location=area)
        place.save()
      for skill in skills:
        js = JobSearch(search_string=skill)
        js.save()
      
      logger.info("Location and job search data created.")

    def run_seed(self, mode):
      """ Seed database based on mode

      :param mode: refresh / clear 
      :return:
      """
      # Clear data from tables
      self.clear_data()
      if mode == MODE_CLEAR:
          return

      self.create_data()