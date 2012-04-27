"""
Indivo Model for HealthActionPlan
"""

from fact import Fact
from actionbase import ActionObject
from django.db import models
from django.conf import settings

class StopConditions(ActionObject):
    action_id = models.IntegerField()
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
    operator = models.CharField(max_length=200, null=True)
    operator_type = models.CharField(max_length=200, null=True)
    operator_value = models.CharField(max_length=200, null=True)
    operator_abbrev = models.CharField(max_length=20, null=True)
    detail = models.CharField(max_length=200, null=True)
    detail_type = models.CharField(max_length=200, null=True)
    detail_value = models.CharField(max_length=200, null=True)
    detail_abbrev = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return "StopConditions: %s" % (self.id, )


class Targets(ActionObject):
    action_id = models.IntegerField()
    name = models.CharField(max_length=200)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)
    minimumValue_textvalue = models.CharField(null=True, max_length=100)
    minimumValue_value = models.CharField(null=True, max_length=20)
    minimumValue_unit = models.CharField(null=True, max_length=40)
    minimumValue_unit_type = models.CharField(null=True, max_length=200)
    minimumValue_unit_value = models.CharField(null=True, max_length=20)
    minimumValue_unit_abbrev = models.CharField(null=True, max_length=20)
    maximumValue_textvalue = models.CharField(null=True, max_length=100)
    maximumValue_value = models.CharField(null=True, max_length=20)
    maximumValue_unit = models.CharField(null=True, max_length=40)
    maximumValue_unit_type = models.CharField(null=True, max_length=200)
    maximumValue_unit_value = models.CharField(null=True, max_length=20)
    maximumValue_unit_abbrev = models.CharField(null=True, max_length=20)
    securityLevel = models.CharField(max_length=200, null=True)
    securityLevel_type = models.CharField(max_length=200, null=True)
    securityLevel_value = models.CharField(max_length=200, null=True)
    securityLevel_abbrev = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return "Targets: %s" % (self.id, )


class MeasurementPlans(ActionObject):
    action_id = models.IntegerField()
    name = models.CharField(max_length=200)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=200, null=True)
    type_type = models.CharField(max_length=200, null=True)
    type_value = models.CharField(max_length=200, null=True)
    type_abbrev = models.CharField(max_length=20, null=True)
    aggregationFunction = models.CharField(max_length=200, null=True)
    aggregationFunction_type = models.CharField(max_length=200, null=True)
    aggregationFunction_value = models.CharField(max_length=200, null=True)
    aggregationFunction_abbrev = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return "MeasurementPlans: %s" % (self.id, )


class DevicePlans(ActionObject):
    action_id = models.IntegerField()
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
    instructions = models.TextField(null=True)

    def __unicode__(self):
        return "DevicePlans: %s" % (self.id, )


class MedicationPlans(ActionObject):
    action_id = models.IntegerField()
    name = models.CharField(max_length=200)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)
    indication = models.CharField(max_length=200)
    dose_textvalue = models.CharField(null=True, max_length=100)
    dose_value = models.CharField(null=True, max_length=20)
    dose_unit = models.CharField(null=True, max_length=40)
    dose_unit_type = models.CharField(null=True, max_length=200)
    dose_unit_value = models.CharField(null=True, max_length=20)
    dose_unit_abbrev = models.CharField(null=True, max_length=20)
    route = models.CharField(max_length=200, null=True)
    route_type = models.CharField(max_length=200, null=True)
    route_value = models.CharField(max_length=200, null=True)
    route_abbrev = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return "MedicationPlans: %s" % (self.id, )


class Actions(ActionObject):
    action_type = models.CharField(max_length=11)
    state = models.CharField(max_length=5)
    healthactionplan_id = models.CharField(max_length=200)
    position = models.CharField(max_length=200, null=True)
    position_type = models.CharField(max_length=200, null=True)
    position_value = models.CharField(max_length=200, null=True)
    position_abbrev = models.CharField(max_length=20, null=True)
    # repeatCount should only appear if action_type is "ActionGroup"
    repeatCount = models.IntegerField(null=True)
    # The remaining fields should only appear if action_type is "ActionStep"
    name = models.CharField(max_length=200)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=200, null=True)
    type_type = models.CharField(max_length=200, null=True)
    type_value = models.CharField(max_length=200, null=True)
    type_abbrev = models.CharField(max_length=20, null=True)
    additionalDetails = models.CharField(max_length=1000, null=True)
    instructions = models.TextField(null=True)

    def __unicode__(self):
        return "Actions: %s" % (self.id, )


class HealthActionPlan(Fact):
    name = models.CharField(max_length=200)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)
    planType = models.CharField(max_length=200)
    plannedBy = models.CharField(max_length=200)
    datePlanned = models.DateTimeField()
    dateExpires = models.DateTimeField(null=True)
    indication = models.CharField(max_length=200)
    instructions = models.CharField(max_length=1000, null=True)
    system = models.CharField(max_length=200, null=True)
    system_type = models.CharField(max_length=200, null=True)
    system_value = models.CharField(max_length=200, null=True)
    system_abbrev = models.CharField(max_length=20, null=True)
    actions = models.TextField()

    def __unicode__(self):
        return 'HealthActionPlan: %s' % (self.id, )
