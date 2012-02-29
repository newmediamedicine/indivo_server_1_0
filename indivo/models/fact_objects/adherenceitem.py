"""
Indivo Model for AdherenceItem
"""

from fact import Fact
from django.db import models
from django.conf import settings

class AdherenceItem(Fact):
  name=models.CharField(max_length=200)
  name_type=models.CharField(max_length=200, null=True)
  name_value=models.CharField(max_length=200, null=True)
  name_abbrev=models.CharField(max_length=20, null=True)
  reported_by=models.CharField(max_length=200)
  date_reported=models.DateTimeField(null=True)
  recurrence_index=models.IntegerField(null=True)
  adherence=models.CharField(max_length=200)
  nonadherence_reason=models.CharField(max_length=200, null=True)

  def __unicode__(self):
    return 'AdherenceItem %s' % self.id
