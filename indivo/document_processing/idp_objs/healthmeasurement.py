from indivo.lib import iso8601
from indivo.models import HealthMeasurement

XML = 'xml'
DOM = 'dom'

class IDP_HealthMeasurement:

  def post_data(self, name=None,
                      name_type=None,
                      name_value=None,
                      name_abbrev=None,
                      measuredBy=None,
                      dateMeasuredStart=None,
                      dateMeasuredEnd=None,
                      result_textvalue=None,
                      result_value=None,
                      result_unit=None,
                      result_unit_type=None,
                      result_unit_value=None,
                      result_unit_abbrev=None,
                      site=None,
                      position=None,
                      technique=None,
                      comments=None):
    """
    SZ: More error checking needs to be performed in this method
    """
    if dateMeasuredStart: dateMeasuredStart = iso8601.parse_date(dateMeasuredStart)
    if dateMeasuredEnd: dateMeasuredEnd = iso8601.parse_date(dateMeasuredEnd)

    try:
      healthmeasurement_obj = HealthMeasurement.objects.create(name=name,
                                                               name_type=name_type,
                                                               name_value=name_value,
                                                               name_abbrev=name_abbrev,
                                                               measuredBy=measuredBy,
                                                               dateMeasuredStart=dateMeasuredStart,
                                                               dateMeasuredEnd=dateMeasuredEnd,
                                                               result_textvalue=result_textvalue,
                                                               result_value=result_value,
                                                               result_unit=result_unit,
                                                               result_unit_type=result_unit_type,
                                                               result_unit_value=result_unit_value,
                                                               result_unit_abbrev=result_unit_abbrev,
                                                               site=site,
                                                               position=position,
                                                               technique=technique,
                                                               comments=comments)

      return healthmeasurement_obj
    except Exception, e:
      raise ValueError("problem processing healthmeasurement report " + str(e))
