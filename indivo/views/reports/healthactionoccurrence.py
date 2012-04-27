"""
Indivo Views -- HealthActionOccurrence
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import HealthActionOccurrence

HEALTHACTIONOCCURRENCE_FILTERS = {
    DEFAULT_ORDERBY : ('created_at', DATE),
    'name': ('name', STRING),
    'name_type' : ('name_type', STRING),
    'name_value' : ('name_value', STRING),
    'name_abbrev' : ('name_abbrerv', STRING),
    'recurrenceIndex': ('recurrenceIndex', NUMBER)
}

HEALTHACTIONOCCURRENCE_TEMPLATE = 'reports/healthactionoccurrence.xml'

def healthactionoccurrence_list(*args, **kwargs):
    """For 1:1 mapping of URLs to views. Calls _healthactionoccurrence_list"""
    return _healthactionoccurrence_list(*args, **kwargs)

def carenet_healthactionoccurrence_list(*args, **kwargs):
    """For 1:1 mapping of URLs to views. Calls _healthactionoccurrence_list"""
    return _healthactionoccurrence_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _healthactionoccurrence_list(request, group_by, date_group, aggregate_by,
                                 limit, offset, order_by,
                                 status, date_range, filters,
                                 record=None, carenet=None):
    q = FactQuery(HealthActionOccurrence, HEALTHACTIONOCCURRENCE_FILTERS, 
                  group_by, date_group, aggregate_by,
                  limit, offset, order_by,
                  status, date_range, filters,
                  record, carenet)
    try:
        return q.render(HEALTHACTIONOCCURRENCE_TEMPLATE)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))
