"""
Indivo Model for Medication Order
"""

from fact import Fact
from django.db import models
from django.conf import settings

class MedicationOrder(Fact):
  name = models.CharField(max_length=200)
  name_type = models.CharField(max_length=200, null=True)
  name_value = models.CharField(max_length=200, null=True)
  name_abbrev = models.CharField(max_length=20, null=True)
  order_type=models.CharField(null=True, max_length=200)
  ordered_by=models.CharField(null=True, max_length=200)
  date_ordered=models.DateTimeField(null=True)
  date_expires=models.DateTimeField(null=True)
  indication=models.TextField(null=True)
  amountordered_unit=models.CharField(null=True, max_length=100)
  amountordered_textvalue=models.CharField(null=True, max_length=20)
  amountordered_value=models.CharField(null=True, max_length=40)
  amountordered_unit_type=models.CharField(null=True, max_length=200)
  amountordered_unit_value=models.CharField(null=True, max_length=20)
  amountordered_unit_abbrev=models.CharField(null=True, max_length=20)
  refills=models.IntegerField(null=True)
  substitution_permitted=models.NullBooleanField()
  instructions=models.TextField(null=True)

  def __unicode__(self):
    return 'MedicationOrder %s' % self.id
