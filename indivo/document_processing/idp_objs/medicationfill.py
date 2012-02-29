from indivo.lib import iso8601
from indivo.models import MedicationFill

XML = 'xml'
DOM = 'dom'

class IDP_MedicationFill:

  def post_data(self, name=None,
                      name_type=None,
                      name_value=None,
                      name_abbrev=None,
                      filledBy=None,
                      dateFilled=None,
                      amountFilled_unit=None,
                      amountFilled_textvalue=None,
                      amountFilled_value=None,
                      amountFilled_unit_type=None, 
                      amountFilled_unit_value=None,
                      amountFilled_unit_abbrev=None,
                      ndc=None,
                      ndc_type=None,
                      ndc_value=None,
                      ndc_abbrev=None,
                      fillSequenceNumber=None,
                      lotNumber=None,
                      refillsRemaining=None,
                      instructions=None):


    """
    SZ: More error checking needs to be performed in this method
    """

    try:
      if dateFilled:
        """
        Elliot: 3/4 changed parse_utc_date to parse_date to handle XML:datetime
        """
        dateFilled = iso8601.parse_date(dateFilled)

      medicationfill_obj = MedicationFill.objects.create(   
                      name=name,
                      name_type=name_type,
                      name_value=name_value,
                      name_abbrev=name_abbrev,
                      filled_by=filledBy,
                      date_filled=dateFilled,
                      amountfilled_unit=amountFilled_unit,
                      amountfilled_textvalue=amountFilled_textvalue,
                      amountfilled_value=amountFilled_value,
                      amountfilled_unit_type=amountFilled_unit_type, 
                      amountfilled_unit_value=amountFilled_unit_value,
                      amountfilled_unit_abbrev=amountFilled_unit_abbrev,
                      ndc=ndc,
                      ndc_type=ndc_type,
                      ndc_value=ndc_value,
                      ndc_abbrev=ndc_abbrev,
                      fill_sequence_number=fillSequenceNumber,
                      lot_number=lotNumber,
                      refills_remaining=refillsRemaining,
                      instructions=instructions)

      return medicationfill_obj
    except Exception, e:
      raise ValueError("problem processing medicationfill report " + str(e))

