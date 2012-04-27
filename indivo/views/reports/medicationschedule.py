"""
Indivo Views -- MedicationSchedule
"""

from django.http import HttpResponseBadRequest, HttpResponse
from indivo.lib.view_decorators import marsloader, DEFAULT_ORDERBY
from indivo.lib.query import FactQuery, DATE, STRING, NUMBER
from indivo.models import MedicationSchedule

MEDICATIONSCHEDULE_FILTERS = {
    DEFAULT_ORDERBY : ('created_at', DATE),
    'name': ('name', STRING),
    'name_type' : ('name_type', STRING),
    'name_value' : ('name_value', STRING),
    'name_abbrev' : ('name_abbrerv', STRING),    
    'scheduledBy': ('scheduledBy', STRING),
    'dateScheduled': ('dateScheduled', DATE),
    'dateStart': ('dateStart', DATE),
    'dateEnd': ('dateEnd', DATE),
    'recurrenceRule_frequency': ('recurrenceRule_frequency', STRING),
    'recurrenceRule_frequency_type' : ('recurrenceRule_frequency_type', STRING),
    'recurrenceRule_frequency_value' : ('recurrenceRule_frequency_value', STRING),
    'recurrenceRule_frequency_abbrev' : ('recurrenceRule_frequency_abbrerv', STRING),    
    'recurrenceRule_interval': ('recurrenceRule_interval', STRING),
    'recurrenceRule_interval_type' : ('recurrenceRule_interval_type', STRING),
    'recurrenceRule_interval_value' : ('recurrenceRule_interval_value', STRING),
    'recurrenceRule_interval_abbrev' : ('recurrenceRule_interval_abbrerv', STRING),    
    'recurrenceRule_count': ('recurrenceRule_count', NUMBER),
    'dose_textvalue' : ('dose_textvalue', STRING),
    'dose_value' : ('dose_value', STRING),
    'dose_unit' : ('dose_unit', STRING),
    'dose_unit_type' : ('dose_unit_type', STRING),
    'dose_unit_value' : ('dose_unit_value', STRING),
    'dose_unit_abbrev' : ('dose_unit_abbrerv', STRING),
    'instructions': ('instructions', STRING)
}

MEDICATIONSCHEDULE_TEMPLATE = 'reports/medicationschedule.xml'

def medicationschedule_list(*args, **kwargs):
    """For 1:1 mapping of URLs to views. Calls _medicationschedule_list"""
    return _medicationschedule_list(*args, **kwargs)

def carenet_medicationschedule_list(*args, **kwargs):
    """For 1:1 mapping of URLs to views. Calls _medicationschedule_list"""
    return _medicationschedule_list(*args, **kwargs)

@marsloader(query_api_support=True)
def _medicationschedule_list(request, group_by, date_group, aggregate_by,
                             limit, offset, order_by,
                             status, date_range, filters,
                             record=None, carenet=None):
    q = FactQuery(MedicationSchedule, MEDICATIONSCHEDULE_FILTERS, 
                  group_by, date_group, aggregate_by,
                  limit, offset, order_by,
                  status, date_range, filters,
                  record, carenet)
    try:
        return q.render(MEDICATIONSCHEDULE_TEMPLATE)
    except ValueError as e:
        return HttpResponseBadRequest(str(e))
