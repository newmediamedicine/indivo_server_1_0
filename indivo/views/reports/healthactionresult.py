"""
Indivo Views -- HealthActionResult Message
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import HealthActionResult

HEALTHACTIONRESULT_FILTERS = {
  'name' : ('name', STRING),
  'name_type' : ('name_type', STRING),
  'name_value' : ('name_value', STRING),
  'name_abbrev' : ('name_abbrerv', STRING),
  'planType' : ('planType', STRING),
  'reportedBy' : ('reportedBy', STRING),
  'dateReported' : ('dateReported', DATE),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

HEALTHACTIONRESULT_TEMPLATE = 'reports/healthactionresult.xml'

def healthactionresult_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _healthactionresult_list"""
  return _healthactionresult_list(*args, **kwargs)

def carenet_healthactionresult_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _healthactionresult_list"""
  return _healthactionresult_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _healthactionresult_list(request, group_by, date_group, aggregate_by,
             limit, offset, order_by,
             status, date_range, filters,
             record=None, carenet=None):
  q = FactQuery(HealthActionResult, HEALTHACTIONRESULT_FILTERS, 
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)
  try:
    return q.render(HEALTHACTIONRESULT_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))
