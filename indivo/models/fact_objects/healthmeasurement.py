"""
Indivo Models for HealthMeasurement
"""

from fact import Fact
from django.db import models
from django.conf import settings

class HealthMeasurement(Fact):
    name = models.CharField(max_length=200)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)
    measuredBy = models.CharField(max_length=200, null=True)
    dateMeasuredStart = models.DateTimeField()
    dateMeasuredEnd = models.DateTimeField(null=True)
    result_textvalue = models.CharField(null=True, max_length=100)
    result_value = models.CharField(null=True, max_length=20)
    result_unit = models.CharField(null=True, max_length=40)
    result_unit_type = models.CharField(null=True, max_length=200)
    result_unit_value = models.CharField(null=True, max_length=20)
    result_unit_abbrev = models.CharField(null=True, max_length=20)
    site = models.CharField(max_length=200, null=True)
    position = models.CharField(max_length=200, null=True)
    technique = models.CharField(max_length=200, null=True)
    comments = models.CharField(max_length=1000, null=True)

    def __unicode__(self):
        return 'HealthMeasurement %s' % self.id

