"""
Indivo Model for Equipment Schedule Item
"""

from fact import Fact
from django.db import models
from django.conf import settings

class EquipmentScheduleItem(Fact):
  name = models.CharField(max_length=200)
  name_type = models.CharField(max_length=200, null=True)
  name_value = models.CharField(max_length=200, null=True)
  name_abbrev = models.CharField(max_length=20, null=True)
  scheduled_by = models.CharField(max_length=200)
  date_scheduled = models.DateTimeField(null=True)
  date_start = models.DateTimeField(null=True)
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
  instructions = models.TextField(null=True)


  def __unicode__(self):
    return 'EquipmentScheduleItem %s' % self.id
