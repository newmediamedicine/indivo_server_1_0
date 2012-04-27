"""
Indivo Model for Device
"""

from fact import Fact
from django.db import models
from django.conf import settings

class Device(Fact):
    name = models.CharField(max_length=200)
    name_type = models.CharField(max_length=200, null=True)
    name_value = models.CharField(max_length=200, null=True)
    name_abbrev = models.CharField(max_length=20, null=True)
    identity = models.CharField(max_length=200, null=True)
    identity_type = models.CharField(max_length=200, null=True)
    identity_value = models.CharField(max_length=200, null=True)
    identity_abbrev = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=200, null=True)
    type_type = models.CharField(max_length=200, null=True)
    type_value = models.CharField(max_length=200, null=True)
    type_abbrev = models.CharField(max_length=20, null=True)
    indication = models.CharField(max_length=200, null=True)
    vendor = models.CharField(max_length=200, null=True)
    vendor_type = models.CharField(max_length=200, null=True)
    vendor_value = models.CharField(max_length=200, null=True)
    vendor_abbrev = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=200, null=True)
    specification = models.CharField(max_length=200, null=True)
    certification = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return 'Device %s' % self.id

