"""
Indivo Views -- Medication Order
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import MedicationOrder

MEDICATIONORDER_FILTERS = {
  DEFAULT_ORDERBY : ('created_at', DATE)
}

MEDICATIONORDER_TEMPLATE = 'reports/medicationorder.xml'

def medicationorder_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _medicationorder_list"""
  return _medicationorder_list(*args, **kwargs)

def carenet_medicationorder_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _medicationorder_list"""
  return _medicationorder_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _medicationorder_list(request, group_by, date_group, aggregate_by,
             limit, offset, order_by,
             status, date_range, filters,
             record=None, carenet=None):
  q = FactQuery(MedicationOrder, MEDICATIONORDER_FILTERS, 
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)
  try:
    return q.render(MEDICATIONORDER_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))
