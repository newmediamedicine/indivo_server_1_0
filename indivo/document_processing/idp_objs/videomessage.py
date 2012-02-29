from indivo.lib import iso8601
from indivo.models import VideoMessage

XML = 'xml'
DOM = 'dom'

class IDP_VideoMessage:

  def post_data(self, fileId=None, 
                      storageType=None, 
                      subject=None, 
                      from_str=None,
                      dateRecorded=None,
                      dateSent=None):

    """
    SZ: More error checking needs to be performed in this method
    """

    try:
     
      if dateRecorded:
        dateRecorded = iso8601.parse_date(dateRecorded)
      if dateSent:
        dateSent = iso8601.parse_date(dateSent)

      videomessage_obj = VideoMessage.objects.create( 
                      file_id=fileId,
                      storage_type=storageType,   
                      subject=subject, 
                      from_str=from_str,
                      date_recorded=dateRecorded,
                      date_sent=dateSent)

      return videomessage_obj
    except Exception, e:
      raise ValueError("problem processing videomessage report " + str(e))
