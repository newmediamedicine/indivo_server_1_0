"""
Indivo Model for Vitals
"""

from fact import Fact
from django.db import models
from django.conf import settings

class Vitals(Fact):
  name = models.CharField(max_length=100)
  name_type = models.CharField(max_length=80, null=True)
  name_value = models.CharField(max_length=40, null=True)
  name_abbrev = models.CharField(max_length=20, null=True)
  measured_by=models.CharField(max_length=200, null=True)
  date_measured_start=models.DateTimeField(null=True)
  date_measured_end=models.DateTimeField(null=True)
  result_unit=models.CharField(max_length=100, null=True)
  result_textvalue=models.CharField(max_length=5000, null=True)
  result_value=models.CharField(max_length=200, null=True)
  result_unit_type=models.CharField(max_length=200, null=True)
  result_unit_value=models.CharField(max_length=200, null=True)
  result_unit_abbrev=models.CharField(max_length=200, null=True)
  site = models.CharField(max_length=40, null=True)
  position = models.CharField(max_length=40, null=True)
  technique=models.CharField(max_length=200, null=True)
  comments = models.TextField(null=True)

  def __unicode__(self):
    return 'Vitals %s' % self.id
