"""
Indivo Views -- Device
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import Device

DEVICE_FILTERS = {
    DEFAULT_ORDERBY : ('created_at', DATE),
    'name' : ('name', STRING),
    'name_type' : ('name_type', STRING),
    'name_value' : ('name_value', STRING),
    'name_abbrev' : ('name_abbrerv', STRING),
    'identity' : ('identity', STRING),
    'identity_type' : ('identity_type', STRING),
    'identity_value' : ('identity_value', STRING),
    'identity_abbrev' : ('identity_abbrerv', STRING),
    'type' : ('type', STRING),
    'type_type' : ('type_type', STRING),
    'type_value' : ('type_value', STRING),
    'type_abbrev' : ('type_abbrerv', STRING),
    'indication' : ('indication', STRING),
    'vendor' : ('vendor', STRING),
    'vendor_type' : ('vendor_type', STRING),
    'vendor_value' : ('vendor_value', STRING),
    'vendor_abbrev' : ('vendor_abbrerv', STRING),
    'description' : ('description', STRING),
    'specification' : ('specification', STRING),
    'certification' : ('certification', STRING),
}

DEVICE_TEMPLATE = 'reports/device.xml'

def device_list(*args, **kwargs):
    """For 1:1 mapping of URLs to views. Calls _device_list"""
    return _device_list(*args, **kwargs)

def carenet_greetings_list(*args, **kwargs):
    """For 1:1 mapping of URLs to views. Calls _device_list"""
    return _device_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _device_list(request, group_by, date_group, aggregate_by,
                 limit, offset, order_by,
                 status, date_range, filters,
                 record=None, carenet=None):
    q = FactQuery(Device, DEVICE_FILTERS, 
                  group_by, date_group, aggregate_by,
                  limit, offset, order_by,
                  status, date_range, filters,
                  record, carenet)
    try:
        return q.render(DEVICE_TEMPLATE)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))
