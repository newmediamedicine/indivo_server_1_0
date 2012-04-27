from indivo.lib import iso8601
from indivo.models import Device

XML = 'xml'
DOM = 'dom'

class IDP_Device:

  def post_data(self, name=None,
                      name_type=None,
                      name_value=None,
                      name_abbrev=None,
                      identity=None,
                      identity_type=None,
                      identity_value=None,
                      identity_abbrev=None,
                      type=None,
                      type_type=None,
                      type_value=None,
                      type_abbrev=None,
                      indication=None,
                      vendor=None,
                      vendor_type=None,
                      vendor_value=None,
                      vendor_abbrev=None,
                      description=None,
                      specification=None,
                      certification=None):
    """
    SZ: More error checking needs to be performed in this method
    """

    try:
      device_obj = Device.objects.create( name=name,
                                          name_type=name_type,
                                          name_value=name_value,
                                          name_abbrev=name_abbrev,
                                          identity=identity,
                                          identity_type=identity_type,
                                          identity_value=identity_value,
                                          identity_abbrev=identity_abbrev,
                                          type=type,
                                          type_type=type_type,
                                          type_value=type_value,
                                          type_abbrev=type_abbrev,
                                          indication=indication,
                                          vendor=vendor,
                                          vendor_type=vendor_type,
                                          vendor_value=vendor_value,
                                          vendor_abbrev=vendor_abbrev,
                                          description=description,
                                          specification=specification,
                                          certification=certification)

      return device_obj
    except Exception, e:
      raise ValueError("problem processing device report " + str(e))
