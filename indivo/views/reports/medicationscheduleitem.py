"""
Indivo Views -- Medication Schedule Item
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import MedicationScheduleItem

MEDICATIONSCHEDULEITEM_FILTERS = {
  DEFAULT_ORDERBY : ('created_at', DATE)
}

MEDICATIONSCHEDULEITEM_TEMPLATE = 'reports/medicationscheduleitem.xml'

def medicationscheduleitem_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _medicationscheduleitem_list"""
  return _medicationscheduleitem_list(*args, **kwargs)

def carenet_medicationscheduleitem_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _medicationscheduleitem_list"""
  return _medicationscheduleitem_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _medicationscheduleitem_list(request, group_by, date_group, aggregate_by,
             limit, offset, order_by,
             status, date_range, filters,
             record=None, carenet=None):
  q = FactQuery(MedicationScheduleItem, MEDICATIONSCHEDULEITEM_FILTERS, 
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)
  try:
    return q.render(MEDICATIONSCHEDULEITEM_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))
