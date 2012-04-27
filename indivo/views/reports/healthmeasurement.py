"""
Indivo Views -- HealthMeasurement
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import HealthMeasurement

HEALTHMEASUREMENT_FILTERS = {
    DEFAULT_ORDERBY : ('created_at', DATE),
    'name' : ('name', STRING),
    'name_type' : ('name_type', STRING),
    'name_value' : ('name_value', STRING),
    'name_abbrev' : ('name_abbrerv', STRING),
    'measuredBy' : ('measuredBy', STRING),
    'dateMeasuredStart': ('dateMeasuredStart', DATE),
    'dateMeasuredEnd': ('dateMeasuredEnd', DATE),
    'result_textvalue' : ('result_textvalue', STRING),
    'result_value' : ('result_value', STRING),
    'result_unit' : ('result_unit', STRING),
    'result_unit_type' : ('result_unit_type', STRING),
    'result_unit_value' : ('result_unit_value', STRING),
    'result_unit_abbrev' : ('result_unit_abbrerv', STRING),
    'site' : ('site', STRING),
    'position' : ('position', STRING),
    'technique' : ('technique', STRING),
    'comments' : ('comments', STRING),
}

HEALTHMEASUREMENT_TEMPLATE = 'reports/healthmeasurement.xml'

def healthmeasurement_list(*args, **kwargs):
    """For 1:1 mapping of URLs to views. Calls _healthmeasurement_list"""
    return _healthmeasurement_list(*args, **kwargs)

def carenet_healthmeasurement_list(*args, **kwargs):
    """For 1:1 mapping of URLs to views. Calls _healthmeasurement_list"""
    return _healthmeasurement_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _healthmeasurement_list(request, group_by, date_group, aggregate_by,
                            limit, offset, order_by,
                            status, date_range, filters,
                            record=None, carenet=None):
    q = FactQuery(HealthMeasurement, HEALTHMEASUREMENT_FILTERS, 
                  group_by, date_group, aggregate_by,
                  limit, offset, order_by,
                  status, date_range, filters,
                  record, carenet)
    try:
        return q.render(HEALTHMEASUREMENT_TEMPLATE)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))
