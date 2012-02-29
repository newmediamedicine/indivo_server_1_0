"""
Indivo Views -- Adherence Item
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import AdherenceItem

ADHERENCEITEM_FILTERS = {
  DEFAULT_ORDERBY : ('created_at', DATE)
}

ADHERENCEITEM_TEMPLATE = 'reports/adherenceitem.xml'

def adherenceitem_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _adherenceitem_list"""
  return _adherenceitem_list(*args, **kwargs)

def carenet_adherenceitem_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _adherenceitem_list"""
  return _adherenceitem_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _adherenceitem_list(request, group_by, date_group, aggregate_by,
             limit, offset, order_by,
             status, date_range, filters,
             record=None, carenet=None):
  q = FactQuery(AdherenceItem, ADHERENCEITEM_FILTERS, 
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)
  try:
    return q.render(ADHERENCEITEM_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))
