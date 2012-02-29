"""
Indivo Model for Medication Administration
"""

from fact import Fact
from django.db import models
from django.conf import settings

class MedicationAdministration(Fact):
  name = models.CharField(max_length=200)
  name_type = models.CharField(max_length=200, null=True)
  name_value = models.CharField(max_length=200, null=True)
  name_abbrev = models.CharField(max_length=20, null=True)
  reported_by=models.CharField(null=True, max_length=200)
  date_reported=models.DateTimeField(null=True)
  date_administered=models.DateTimeField(null=True)
  amountadministered_unit=models.CharField(null=True, max_length=100)
  amountadministered_textvalue=models.CharField(null=True, max_length=20)
  amountadministered_value=models.CharField(null=True, max_length=40)
  amountadministered_unit_type=models.CharField(null=True, max_length=200)
  amountadministered_unit_value=models.CharField(null=True, max_length=20)
  amountadministered_unit_abbrev=models.CharField(null=True, max_length=20)
  amountremaining_unit=models.CharField(null=True, max_length=100)
  amountremaining_textvalue=models.CharField(null=True, max_length=20)
  amountremaining_value=models.CharField(null=True, max_length=40)
  amountremaining_unit_type=models.CharField(null=True, max_length=200)
  amountremaining_unit_value=models.CharField(null=True, max_length=20)
  amountremaining_unit_abbrev=models.CharField(null=True, max_length=20)


  def __unicode__(self):
    return 'MedicationAdministration %s' % self.id
