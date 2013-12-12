#!/usr/bin/python

import os 
import sys 
from xml.dom import minidom 
import datasections 

verbosity = False 
if len(sys.argv[1:]) > 0 and sys.argv[1] == '-v':
  verbosity = True
  
data_file = 'indivo_data.xml' 
if len(sys.argv[2:]) > 0:
  data_file = sys.argv[2] 

bf_prefix = '' 
if os.path.dirname(__file__):
  bf_prefix = os.path.dirname(__file__) + '/' 
data_file = bf_prefix + data_file 

if os.path.isfile(data_file):
  f = open(data_file)
  lines = []
  for line in f:
    lines.append(line.strip())
  dom = minidom.parseString(''.join(lines))
  for root in dom.childNodes:
    for section in root.childNodes:
      try:
        # Note the nodeName, className and fileName relationship
        if section and hasattr(section, 'nodeName'):
          if hasattr(datasections, section.nodeName):
            class_name = section.nodeName.capitalize()
            seclib = getattr(datasections, section.nodeName)
            if hasattr(seclib, class_name):
              getattr(seclib, class_name)(section, verbosity)
      except ImportError:
        pass 
else:
  print "Data file " + data_file + " not found"
