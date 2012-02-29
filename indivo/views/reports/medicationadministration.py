"""
Indivo Views -- Medication Administration
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import MedicationAdministration

MEDICATIONADMINISTRATION_FILTERS = {
  DEFAULT_ORDERBY : ('created_at', DATE)
}

MEDICATIONADMINISTRATION_TEMPLATE = 'reports/medicationadministration.xml'

def medicationadministration_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _medicationadministration_list"""
  return _medicationadministration_list(*args, **kwargs)

def carenet_medicationadministration_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _medicationadministration_list"""
  return _medicationadministration_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _medicationadministration_list(request, group_by, date_group, aggregate_by,
             limit, offset, order_by,
             status, date_range, filters,
             record=None, carenet=None):
  q = FactQuery(MedicationAdministration, MEDICATIONADMINISTRATION_FILTERS, 
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)
  try:
    return q.render(MEDICATIONADMINISTRATION_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))
