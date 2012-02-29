"""
Indivo Views -- Equipment Schedule Item
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import EquipmentScheduleItem

EQUIPMENTSCHEDULEITEM_FILTERS = {
  DEFAULT_ORDERBY : ('created_at', DATE)
}

EQUIPMENTSCHEDULEITEM_TEMPLATE = 'reports/equipmentscheduleitem.xml'

def equipmentscheduleitem_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _equipmentscheduleitem_list"""
  return _equipmentscheduleitem_list(*args, **kwargs)

def carenet_equipmentscheduleitem_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _equipmentscheduleitem_list"""
  return _equipmentscheduleitem_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _equipmentscheduleitem_list(request, group_by, date_group, aggregate_by,
             limit, offset, order_by,
             status, date_range, filters,
             record=None, carenet=None):
  q = FactQuery(EquipmentScheduleItem, EQUIPMENTSCHEDULEITEM_FILTERS, 
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)
  try:
    return q.render(EQUIPMENTSCHEDULEITEM_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))
