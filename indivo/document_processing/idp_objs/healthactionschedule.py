from indivo.lib import iso8601
from indivo.models import HealthActionSchedule

XML = 'xml'
DOM = 'dom'

class IDP_HealthActionSchedule:

  def post_data(self, name=None,
                      name_type=None,
                      name_value=None,
                      name_abbrev=None,
                      scheduledBy=None,
                      dateScheduled=None,
                      dateStart=None,
                      dateEnd=None,
                      recurrenceRule_frequency=None,
                      recurrenceRule_frequency_type=None,
                      recurrenceRule_frequency_value=None,
                      recurrenceRule_frequency_abbrev=None,
                      recurrenceRule_interval=None,
                      recurrenceRule_interval_type=None,
                      recurrenceRule_interval_value=None,
                      recurrenceRule_interval_abbrev=None,
                      recurrenceRule_count=None,
                      dose_textvalue=None,
                      dose_value=None,
                      dose_unit=None,
                      dose_unit_type=None,
                      dose_unit_value=None,
                      dose_unit_abbrev=None,
                      instructions=None):
    """
    SZ: More error checking needs to be performed in this method
    """
    if dateScheduled: dateScheduled = iso8601.parse_date(dateScheduled)
    if dateStart: dateStart = iso8601.parse_date(dateStart)
    if dateEnd: dateEnd = iso8601.parse_date(dateEnd)

    try:
      healthactionschedule_obj = HealthActionSchedule.objects.create(name=name,
                                                                     name_type=name_type,
                                                                     name_value=name_value,
                                                                     name_abbrev=name_abbrev,
                                                                     scheduledBy=scheduledBy,
                                                                     dateScheduled=dateScheduled,
                                                                     dateStart=dateStart,
                                                                     dateEnd=dateEnd,
                                                                     recurrenceRule_frequency=recurrenceRule_frequency,
                                                                     recurrenceRule_frequency_type=recurrenceRule_frequency_type,
                                                                     recurrenceRule_frequency_value=recurrenceRule_frequency_value,
                                                                     recurrenceRule_frequency_abbrev=recurrenceRule_frequency_abbrev,
                                                                     recurrenceRule_interval=recurrenceRule_interval,
                                                                     recurrenceRule_interval_type=recurrenceRule_interval_type,
                                                                     recurrenceRule_interval_value=recurrenceRule_interval_value,
                                                                     recurrenceRule_interval_abbrev=recurrenceRule_interval_abbrev,
                                                                     recurrenceRule_count=recurrenceRule_count,
                                                                     dose_textvalue=dose_textvalue,
                                                                     dose_value=dose_value,
                                                                     dose_unit=dose_unit,
                                                                     dose_unit_type=dose_unit_type,
                                                                     dose_unit_value=dose_unit_value,
                                                                     dose_unit_abbrev=dose_unit_abbrev,
                                                                     instructions=instructions)

      return healthactionschedule_obj
    except Exception, e:
      raise ValueError("problem processing healthactionschedule report " + str(e))
