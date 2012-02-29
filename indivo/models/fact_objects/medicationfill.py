"""
Indivo Model for Medication Fill
"""

from fact import Fact
from django.db import models
from django.conf import settings

class MedicationFill(Fact):
  name = models.CharField(max_length=200)
  name_type = models.CharField(max_length=200, null=True)
  name_value = models.CharField(max_length=200, null=True)
  name_abbrev = models.CharField(max_length=20, null=True)
  filled_by=models.CharField(null=True, max_length=200)
  date_filled=models.DateTimeField(null=True)
  amountfilled_unit=models.CharField(null=True, max_length=100)
  amountfilled_textvalue=models.CharField(null=True, max_length=20)
  amountfilled_value=models.CharField(null=True, max_length=40)
  amountfilled_unit_type=models.CharField(null=True, max_length=200)
  amountfilled_unit_value=models.CharField(null=True, max_length=20)
  amountfilled_unit_abbrev=models.CharField(null=True, max_length=20)
  ndc = models.CharField(max_length=200)
  ndc_type = models.CharField(max_length=200, null=True)
  ndc_value = models.CharField(max_length=200, null=True)
  ndc_abbrev = models.CharField(max_length=20, null=True)
  fill_sequence_number=models.IntegerField(null=True)
  lot_number=models.IntegerField(null=True)
  refills_remaining=models.IntegerField(null=True)
  instructions=models.TextField(null=True)

  def __unicode__(self):
    return 'MedicationFill %s' % self.id
