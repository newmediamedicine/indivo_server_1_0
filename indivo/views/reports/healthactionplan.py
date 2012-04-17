"""
Indivo Views -- HealthActionPlan Message
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import HealthActionPlan

HEALTHACTIONPLAN_FILTERS = {
  'name' : ('name', STRING),
  'name_type' : ('name_type', STRING),
  'name_value' : ('name_value', STRING),
  'name_abbrev' : ('name_abbrerv', STRING),
  'planType' : ('planType', STRING),
  'plannedBy' : ('plannedBy', STRING),
  'datePlanned' : ('datePlanned', DATE),
  'dateExpires' : ('dateExpires', DATE),
  'indication' : ('indication', STRING),
  'instructions' : ('instructions', STRING),
  'system' : ('system', STRING),
  'system_type' : ('system_type', STRING),
  'system_value' : ('system_value', STRING),
  'system_abbrev' : ('system_abbrerv', STRING),
  DEFAULT_ORDERBY : ('created_at', DATE)
}

HEALTHACTIONPLAN_TEMPLATE = 'reports/healthactionplan.xml'

def healthactionplan_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _healthactionplan_list"""
  return _healthactionplan_list(*args, **kwargs)

def carenet_healthactionplan_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _healthactionplan_list"""
  return _healthactionplan_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _healthactionplan_list(request, group_by, date_group, aggregate_by,
             limit, offset, order_by,
             status, date_range, filters,
             record=None, carenet=None):
  q = FactQuery(HealthActionPlan, HEALTHACTIONPLAN_FILTERS, 
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)
  try:
    return q.render(HEALTHACTIONPLAN_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))
