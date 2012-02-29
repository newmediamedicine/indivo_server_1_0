"""
Indivo Model for VideoMessage
"""

from fact import Fact
from django.db import models
from django.conf import settings

class VideoMessage(Fact):
  file_id=models.CharField(max_length=200)
  storage_type=models.CharField(max_length=200)   
  subject=models.CharField(max_length=200) 
  from_str=models.CharField(max_length=200)
  date_recorded=models.DateTimeField(null=True)
  date_sent=models.DateTimeField(null=True)

  def __unicode__(self):
    return 'VideoMessage %s' % self.id
