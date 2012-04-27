from indivo.lib import iso8601
from indivo.models import HealthActionOccurrence

XML = 'xml'
DOM = 'dom'

class IDP_HealthActionOccurrence:

  def post_data(self, name=None,
                      name_type=None,
                      name_value=None,
                      name_abbrev=None,
                      recurrenceIndex=None):
    """
    SZ: More error checking needs to be performed in this method
    """

    try:
      healthactionoccurrence_obj = HealthActionOccurrence.objects.create(name=name,
                                                                         name_type=name_type,
                                                                         name_value=name_value,
                                                                         name_abbrev=name_abbrev,
                                                                         recurrenceIndex=recurrenceIndex)

      return healthactionoccurrence_obj
    except Exception, e:
      raise ValueError("problem processing healthactionoccurrence report " + str(e))
