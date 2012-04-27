"""
Indivo Model for HealthActionOccurrence
"""

from fact import Fact
from django.db import models
from django.conf import settings

class HealthActionOccurrence(Fact):
    name = models.CharField(max_length=200)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)
    recurrenceIndex = models.IntegerField(null=True)

    def __unicode__(self):
        return 'HealthActionOccurrence %s' % self.id

