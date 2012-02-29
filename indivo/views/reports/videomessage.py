"""
Indivo Views -- Video Message
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import VideoMessage

VIDEOMESSAGE_FILTERS = {
  DEFAULT_ORDERBY : ('created_at', DATE)
}

VIDEOMESSAGE_TEMPLATE = 'reports/videomessage.xml'

def videomessage_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _videomessage_list"""
  return _videomessage_list(*args, **kwargs)

def carenet_videomessage_list(*args, **kwargs):
  """For 1:1 mapping of URLs to views. Calls _videomessage_list"""
  return _videomessage_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _videomessage_list(request, group_by, date_group, aggregate_by,
             limit, offset, order_by,
             status, date_range, filters,
             record=None, carenet=None):
  q = FactQuery(VideoMessage, VIDEOMESSAGE_FILTERS, 
                group_by, date_group, aggregate_by,
                limit, offset, order_by,
                status, date_range, filters,
                record, carenet)
  try:
    return q.render(VIDEOMESSAGE_TEMPLATE)
  except ValueError as e:
    return HttpResponseBadRequest(str(e))
