from indivo.lib import iso8601
from indivo.models import MedicationAdministration

XML = 'xml'
DOM = 'dom'

class IDP_MedicationAdministration:

  def post_data(self, name=None,
                      name_type=None,
                      name_value=None,
                      name_abbrev=None,
                      reportedBy=None,
                      dateReported=None,
                      dateAdministered=None,
                      amountAdministered_unit=None,
                      amountAdministered_textvalue=None,
                      amountAdministered_value=None,
                      amountAdministered_unit_type=None, 
                      amountAdministered_unit_value=None,
                      amountAdministered_unit_abbrev=None,
                      amountRemaining_unit=None,
                      amountRemaining_textvalue=None,
                      amountRemaining_value=None,
                      amountRemaining_unit_type=None, 
                      amountRemaining_unit_value=None,
                      amountRemaining_unit_abbrev=None):


    """
    SZ: More error checking needs to be performed in this method
    """

    try:
      if dateReported:
        """
        Elliot: 3/4 changed parse_utc_date to parse_date to handle XML:datetime
        """
        dateReported = iso8601.parse_date(dateReported)

      if dateAdministered:
        """
        Elliot: 3/4 changed parse_utc_date to parse_date to handle XML:datetime
        """
        dateAdministered = iso8601.parse_date(dateAdministered)


      medicationadministration_obj = MedicationAdministration.objects.create(   
                      name=name,
                      name_type=name_type,
                      name_value=name_value,
                      name_abbrev=name_abbrev,
                      reported_by=reportedBy,
                      date_reported=dateReported,
                      date_administered=dateAdministered,
                      amountadministered_unit=amountAdministered_unit,
                      amountadministered_textvalue=amountAdministered_textvalue,
                      amountadministered_value=amountAdministered_value,
                      amountadministered_unit_type=amountAdministered_unit_type, 
                      amountadministered_unit_value=amountAdministered_unit_value,
                      amountadministered_unit_abbrev=amountAdministered_unit_abbrev,
                      amountremaining_unit=amountRemaining_unit,
                      amountremaining_textvalue=amountRemaining_textvalue,
                      amountremaining_value=amountRemaining_value,
                      amountremaining_unit_type=amountRemaining_unit_type, 
                      amountremaining_unit_value=amountRemaining_unit_value,
                      amountremaining_unit_abbrev=amountRemaining_unit_abbrev)


      return medicationadministration_obj
    except Exception, e:
      raise ValueError("problem processing medicationadministration report " + str(e))

