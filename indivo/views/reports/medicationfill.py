"""
Indivo Views -- Medication Fill
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import MedicationFill

MEDICATIONFILL_FILTERS = {
  DEFAULT_ORDERBY : ('created_at', DATE)
}

MEDICATIONFILL_TEMPLATE = 'reports/medicationfill.xml'

def medicationfill_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _medicationfill_list"""
  return _medicationfill_list(*args, **kwargs)

def carenet_medicationfill_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _medicationfill_list"""
  return _medicationfill_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _medicationfill_list(request, group_by, date_group, aggregate_by,
             limit, offset, order_by,
             status, date_range, filters,
             record=None, carenet=None):
  q = FactQuery(MedicationFill, MEDICATIONFILL_FILTERS, 
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)
  try:
    return q.render(MEDICATIONFILL_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))
