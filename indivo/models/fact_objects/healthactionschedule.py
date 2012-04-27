"""
Indivo Model for HealthActionSchedule
"""

from fact import Fact
from django.db import models
from django.conf import settings

class HealthActionSchedule(Fact):
    name = models.CharField(max_length=200)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)
    scheduledBy = models.CharField(max_length=200)
    dateScheduled = models.DateTimeField()
    dateStart = models.DateTimeField()
    dateEnd = models.DateTimeField(null=True)
    recurrenceRule_frequency = models.CharField(max_length=200)
    recurrenceRule_frequency_type = models.CharField(max_length=200, null=True)
    recurrenceRule_frequency_value = models.CharField(max_length=200, null=True)
    recurrenceRule_frequency_abbrev = models.CharField(max_length=20, null=True)
    recurrenceRule_interval = models.CharField(max_length=200, null=True)
    recurrenceRule_interval_type = models.CharField(max_length=200, null=True)
    recurrenceRule_interval_value = models.CharField(max_length=200, null=True)
    recurrenceRule_interval_abbrev = models.CharField(max_length=20, null=True)
    recurrenceRule_count = models.IntegerField(null=True)
    dose_textvalue = models.CharField(null=True, max_length=100)
    dose_value = models.CharField(null=True, max_length=20)
    dose_unit = models.CharField(null=True, max_length=40)
    dose_unit_type = models.CharField(null=True, max_length=200)
    dose_unit_value = models.CharField(null=True, max_length=20)
    dose_unit_abbrev = models.CharField(null=True, max_length=20)
    instructions = models.TextField(null=True)

    def __unicode__(self):
        return 'HealthActionSchedule %s' % self.id

