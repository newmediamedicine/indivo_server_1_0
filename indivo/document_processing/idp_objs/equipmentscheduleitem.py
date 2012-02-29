from indivo.lib import iso8601
from indivo.models import EquipmentScheduleItem

XML = 'xml'
DOM = 'dom'

class IDP_EquipmentScheduleItem:

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
                      recurrenceRule_dateUntil=None,
                      recurrenceRule_count=None,
											instructions=None):

    """
    SZ: More error checking needs to be performed in this method
    """

    try:
      if dateScheduled:
        """
        Elliot: 3/4 changed parse_utc_date to parse_date to handle XML:datetime
        """
        dateScheduled = iso8601.parse_date(dateScheduled)

      if dateStart:
        """
        Elliot: 3/4 changed parse_utc_date to parse_date to handle XML:datetime
        """
        dateStart = iso8601.parse_date(dateStart)

      if dateEnd:
        """
        Elliot: 3/4 changed parse_utc_date to parse_date to handle XML:datetime
        """
        dateEnd = iso8601.parse_date(dateEnd)

      if recurrenceRule_dateUntil:
        """
        Elliot: 3/4 changed parse_utc_date to parse_date to handle XML:datetime
        """
        recurrenceRule_dateUntil = iso8601.parse_date(recurrenceRule_dateUntil)

      equipmentscheduleitem_obj = EquipmentScheduleItem.objects.create(   
                      name=name,
                      name_type=name_type,
                      name_value=name_value,
                      name_abbrev=name_abbrev,
                      scheduled_by=scheduledBy,
											date_scheduled=dateScheduled,
                      date_start=dateStart,
                      date_end=dateEnd,
                      recurrencerule_frequency=recurrenceRule_frequency,
                      recurrencerule_frequency_type=recurrenceRule_frequency_type,
                      recurrencerule_frequency_value=recurrenceRule_frequency_value,
                      recurrencerule_frequency_abbrev=recurrenceRule_frequency_abbrev,
                      recurrencerule_interval=recurrenceRule_interval,
                      recurrencerule_interval_type=recurrenceRule_interval_type,
                      recurrencerule_interval_value=recurrenceRule_interval_value,
                      recurrencerule_interval_abbrev=recurrenceRule_interval_abbrev,
                      recurrencerule_dateuntil=recurrenceRule_dateUntil,
                      recurrencerule_count=recurrenceRule_count,
											instructions=instructions)

      return equipmentscheduleitem_obj
    except Exception, e:
      print "Error: " + str(e)
      raise ValueError("problem processing equipmentscheduleitem report " + str(e))

