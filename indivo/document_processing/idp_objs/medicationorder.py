from indivo.lib import iso8601
from indivo.models import MedicationOrder

XML = 'xml'
DOM = 'dom'

class IDP_MedicationOrder:

  def post_data(self, name=None,
                      name_type=None,
                      name_value=None,
                      name_abbrev=None,
                      orderType=None,
                      orderedBy=None,
                      dateOrdered=None,
                      dateExpires=None,
                      indication=None,
                      amountOrdered_unit=None,
                      amountOrdered_textvalue=None,
                      amountOrdered_value=None,
                      amountOrdered_unit_type=None, 
                      amountOrdered_unit_value=None,
                      amountOrdered_unit_abbrev=None,
                      refills=None,
                      substitutionPermitted=None,
                      instructions=None):

    """
    SZ: More error checking needs to be performed in this method
    """

    try:
      if dateOrdered:
        """
        Elliot: 3/4 changed parse_utc_date to parse_date to handle XML:datetime
        """
        dateOrdered = iso8601.parse_date(dateOrdered)

      if dateExpires:
        """
        Elliot: 3/4 changed parse_utc_date to parse_date to handle XML:datetime
        """
        dateExpires = iso8601.parse_date(dateExpires)


      medicationorder_obj = MedicationOrder.objects.create(   
                      name=name,
                      name_type=name_type,
                      name_value=name_value,
                      name_abbrev=name_abbrev,
                      order_type=orderType,
                      ordered_by=orderedBy,
                      date_ordered=dateOrdered,
                      date_expires=dateExpires,
                      indication=indication,
                      amountordered_unit=amountOrdered_unit,
                      amountordered_textvalue=amountOrdered_textvalue,
                      amountordered_value=amountOrdered_value,
                      amountordered_unit_type=amountOrdered_unit_type, 
                      amountordered_unit_value=amountOrdered_unit_value,
                      amountordered_unit_abbrev=amountOrdered_unit_abbrev,
                      refills=refills,
                      substitution_permitted=substitutionPermitted,
                      instructions=instructions)

      return medicationorder_obj
    except Exception, e:
      raise ValueError("problem processing medicationorder report " + str(e))

