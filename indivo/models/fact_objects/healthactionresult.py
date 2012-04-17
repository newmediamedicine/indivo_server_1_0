"""
Indivo Model for HealthActionPlan
"""

from fact import Fact
from actionbase import ActionObject
from django.db import models
from django.conf import settings

class MedicationAdministrations(ActionObject):
    action_id = models.IntegerField()
    occurrence_id = models.IntegerField(null=True)
    name = models.CharField(max_length=200)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)
    dose = models.CharField(max_length=200)
    dose_type = models.CharField(max_length=200, null=True)
    dose_value = models.CharField(max_length=200, null=True)
    dose_abbrev = models.CharField(max_length=20, null=True)
    route_textvalue = models.CharField(null=True, max_length=100)
    route_value = models.CharField(null=True, max_length=20)
    route_unit = models.CharField(null=True, max_length=40)
    route_unit_type = models.CharField(null=True, max_length=200)
    route_unit_value = models.CharField(null=True, max_length=20)
    route_unit_abbrev = models.CharField(null=True, max_length=20)

    def __unicode__(self):
        return "MedicationAdministrations: %s" % (self.id, )


class DeviceResults(ActionObject):
    action_id = models.IntegerField()
    occurrence_id = models.IntegerField(null=True)
    name = models.CharField(max_length=200, null=True)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=200, null=True)
    type_type = models.CharField(max_length=200, null=True)
    type_value = models.CharField(max_length=200, null=True)
    type_abbrev = models.CharField(max_length=20, null=True)
    value_textvalue = models.CharField(null=True, max_length=100)
    value_value = models.CharField(null=True, max_length=20)
    value_unit = models.CharField(null=True, max_length=40)
    value_unit_type = models.CharField(null=True, max_length=200)
    value_unit_value = models.CharField(null=True, max_length=20)
    value_unit_abbrev = models.CharField(null=True, max_length=20)
    site = models.CharField(max_length=200, null=True)
    site_type = models.CharField(max_length=200, null=True)
    site_value = models.CharField(max_length=200, null=True)
    site_abbrev = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return "DeviceResults: %s" % (self.id, )


class Measurements(ActionObject):
    action_id = models.IntegerField()
    occurrence_id = models.IntegerField(null=True)
    name = models.CharField(max_length=200, null=True)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=200, null=True)
    type_type = models.CharField(max_length=200, null=True)
    type_value = models.CharField(max_length=200, null=True)
    type_abbrev = models.CharField(max_length=20, null=True)
    value_textvalue = models.CharField(null=True, max_length=100)
    value_value = models.CharField(null=True, max_length=20)
    value_unit = models.CharField(null=True, max_length=40)
    value_unit_type = models.CharField(null=True, max_length=200)
    value_unit_value = models.CharField(null=True, max_length=20)
    value_unit_abbrev = models.CharField(null=True, max_length=20)
    aggregationFunction = models.CharField(max_length=200, null=True)
    aggregationFunction_type = models.CharField(max_length=200, null=True)
    aggregationFunction_value = models.CharField(max_length=200, null=True)
    aggregationFunction_abbrev = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return "Measurements: %s" % (self.id, )


class StopConditionResults(ActionObject):
    action_id = models.IntegerField()
    occurrence_id = models.IntegerField(null=True)
    name = models.CharField(max_length=200)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)
    value_textvalue = models.CharField(null=True, max_length=100)
    value_value = models.CharField(null=True, max_length=20)
    value_unit = models.CharField(null=True, max_length=40)
    value_unit_type = models.CharField(null=True, max_length=200)
    value_unit_value = models.CharField(null=True, max_length=20)
    value_unit_abbrev = models.CharField(null=True, max_length=20)

    def __unicode__(self):
        return "StopConditionResults: %s" % (self.id, )


class Occurrences(ActionObject):
    action_id = models.IntegerField()
    startTime = models.DateTimeField(null=True)
    endTime = models.DateTimeField(null=True)
    additionalDetails = models.CharField(max_length=1000, null=True)

    def __unicode__(self):
        return "Occurrences: %s" % (self.id, )


class ActionResults(ActionObject):
    action_type = models.CharField(max_length=17)
    state = models.CharField(max_length=5)
    healthactionresult_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200, null=True)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return "ActionResults: %s" % (self.id, )


class HealthActionResult(Fact):
    name = models.CharField(max_length=200, null=True)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)
    planType = models.CharField(max_length=200, blank=True)
    reportedBy = models.CharField(max_length=200)
    dateReported = models.DateTimeField()
    actions = models.TextField()

    def __unicode__(self):
        return 'HealthActionResult: %s' % (self.id, )
