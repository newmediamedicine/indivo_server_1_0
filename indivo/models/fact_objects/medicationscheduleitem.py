"""
Indivo Model for Medication Schedule Item
"""

from fact import Fact
from django.db import models
from django.conf import settings

class MedicationScheduleItem(Fact):
  name = models.CharField(max_length=200)
  name_type = models.CharField(max_length=200, null=True)
  name_value = models.CharField(max_length=200, null=True)
  name_abbrev = models.CharField(max_length=20, null=True)
  scheduled_by = models.CharField(max_length=200)
  date_scheduled = models.DateTimeField()
  date_start = models.DateTimeField()
  date_end = models.DateTimeField(null=True)
  recurrencerule_frequency = models.CharField(max_length=200)
  recurrencerule_frequency_type = models.CharField(max_length=200, null=True)
  recurrencerule_frequency_value = models.CharField(max_length=200, null=True)
  recurrencerule_frequency_abbrev = models.CharField(max_length=20, null=True)
  recurrencerule_interval = models.CharField(null=True, max_length=200)
  recurrencerule_interval_type = models.CharField(max_length=200, null=True)
  recurrencerule_interval_value = models.CharField(max_length=200, null=True)
  recurrencerule_interval_abbrev = models.CharField(max_length=20, null=True)
  recurrencerule_dateuntil=models.DateTimeField(null=True)
  recurrencerule_count=models.IntegerField(null=True)
  dose_textvalue = models.CharField(null=True, max_length=100)
  dose_value = models.CharField(null=True, max_length=20)
  dose_unit = models.CharField(null=True, max_length=40)
  dose_unit_type = models.CharField(null=True, max_length=200)
  dose_unit_value = models.CharField(null=True, max_length=20)
  dose_unit_abbrev = models.CharField(null=True, max_length=20)
  instructions = models.TextField(null=True)


  def __unicode__(self):
    return 'MedicationScheduleItem %s' % self.id
