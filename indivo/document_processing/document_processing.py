"""
IDP - Indivo Document Processing
"""

import os
import sys
import hashlib
#import libxml2
#import libxslt
from lxml import etree

#from xml.dom import minidom

from indivo.models import DocumentSchema
from django.conf import settings
from django.db import transaction
from django.core.files.base import ContentFile

from idp_objs.allergy                   import IDP_Allergy
from idp_objs.equipment                 import IDP_Equipment
from idp_objs.measurement               import IDP_Measurement
from idp_objs.immunization              import IDP_Immunization
from idp_objs.lab                       import IDP_Lab
from idp_objs.medication                import IDP_Medication
from idp_objs.medicationscheduleitem    import IDP_MedicationScheduleItem
from idp_objs.equipmentscheduleitem     import IDP_EquipmentScheduleItem
from idp_objs.medicationadministration  import IDP_MedicationAdministration
from idp_objs.medicationfill            import IDP_MedicationFill
from idp_objs.medicationorder           import IDP_MedicationOrder
from idp_objs.adherenceitem             import IDP_AdherenceItem
from idp_objs.videomessage              import IDP_VideoMessage
from idp_objs.problem                   import IDP_Problem
from idp_objs.procedure                 import IDP_Procedure
from idp_objs.simple_clinical_note      import IDP_SimpleClinicalNote
from idp_objs.vitals                    import IDP_Vitals
from idp_objs.healthactionplan          import IDP_HealthActionPlan
from idp_objs.healthactionresult        import IDP_HealthActionResult

DP_DOBJ_PROCESS   = 'process'
DP_DOBJ_POST_DATA = 'post_data'
DOC_CLASS_REL     = { 
                  'http://indivo.org/vocab/xml/documents#Allergy'       :   {'class' : 'IDP_Allergy',       'stylesheet' : 'allergy', 'schema' : 'allergy'},
                  'http://indivo.org/vocab/xml/documents#SimpleClinicalNote'  :   {'class' : 'IDP_SimpleClinicalNote',       'stylesheet' : 'simple_clinical_note', 'schema' : 'simplenote'},
                  'http://indivo.org/vocab/xml/documents#Equipment'     :   {'class' : 'IDP_Equipment',     'stylesheet' : 'equipment', 'schema' : 'equipment'},
                  'http://indivo.org/vocab/xml/documents#HBA1C'         :   {'class' : 'IDP_Measurement'},
                  'http://indivo.org/vocab/xml/documents#Immunization'  :   {'class' : 'IDP_Immunization',  'stylesheet' : 'immunization', 'schema' : 'immunization'},
                  'http://indivo.org/vocab/xml/documents#Lab'           :   {'class' : 'IDP_Lab',           'stylesheet' : 'lab', 'schema' : 'lab'},
                  'http://indivo.org/vocab/xml/documents#Medication'    :   {'class' : 'IDP_Medication',    'stylesheet' : 'medication', 'schema' : 'medication'},
                  'http://indivo.org/vocab/xml/documents#MedicationScheduleItem'    :   {'class' : 'IDP_MedicationScheduleItem',    'stylesheet' : 'medicationscheduleitem', 'schema' : 'medicationscheduleitem'},
                  'http://indivo.org/vocab/xml/documents#EquipmentScheduleItem'     :   {'class' : 'IDP_EquipmentScheduleItem',    'stylesheet' : 'equipmentscheduleitem', 'schema' : 'equipmentscheduleitem'},
                  'http://indivo.org/vocab/xml/documents#MedicationAdministration'  :   {'class' : 'IDP_MedicationAdministration',    'stylesheet' : 'medicationadministration', 'schema' : 'medicationadministration'},
                  'http://indivo.org/vocab/xml/documents#MedicationFill'            :   {'class' : 'IDP_MedicationFill',    'stylesheet' : 'medicationfill', 'schema' : 'medicationfill'},
                  'http://indivo.org/vocab/xml/documents#MedicationOrder'           :   {'class' : 'IDP_MedicationOrder',    'stylesheet' : 'medicationorder', 'schema' : 'medicationorder'},
                  'http://indivo.org/vocab/xml/documents#AdherenceItem'             :   {'class' : 'IDP_AdherenceItem',    'stylesheet' : 'adherenceitem', 'schema' : 'adherenceitem'},
                  'http://indivo.org/vocab/xml/documents#VideoMessage'              :   {'class' : 'IDP_VideoMessage',    'stylesheet' : 'videomessage', 'schema' : 'videomessage'},
                  'http://indivo.org/vocab/xml/documents#Problem'       :   {'class' : 'IDP_Problem',       'stylesheet' : 'problem', 'schema' : 'problem'},
                  'http://indivo.org/vocab/xml/documents#Procedure'     :   {'class' : 'IDP_Procedure',     'stylesheet' : 'procedure', 'schema' : 'procedure'},
                  'http://indivo.org/vocab/xml/documents#VitalSign'     :   {'class' : 'IDP_Vitals',        'stylesheet' : 'vitalsign', 'schema' : 'vitals'},
                  'http://indivo.org/vocab/xml/documents#HealthActionPlan'     :   {'class' : 'IDP_HealthActionPlan',        'stylesheet' : 'healthactionplan', 'schema' : 'healthactionplan'},
                  'http://indivo.org/vocab/xml/documents#HealthActionResult'     :   {'class' : 'IDP_HealthActionResult',        'stylesheet' : 'healthactionresult', 'schema' : 'healthactionresult'}
                }

DEFAULT_PREFIX= "http://indivo.org/vocab/xml/documents#"

class DocumentProcessing:

  @classmethod
  def expand_schema(cls, schema):
    """
    go from Allergy to http://indivo.org/vocab/xml/documents#Allergy
    """
    if schema is None:
      return None

    if schema.find(':') > -1 or schema.find('/') > -1:
      return schema
    else:
      return "%s%s" % (DEFAULT_PREFIX, schema)

  def __init__(self, content, mime_type):

    # changed this from heuristic to declared mime type (Ben 1/07/2011)
    # if mime_type is null, we assume it's XML
    self.is_binary      = (mime_type and mime_type != 'application/xml' and mime_type != 'text/xml')

    self.content = content
    if not self.is_binary:
      
      # Validate basic XML Syntax, if required
      if settings.VALIDATE_XML_SYNTAX:
        self.validate_xml_syntax(self.content)

      self.content_dom = self.get_dom(self.get_clean_xml(content))
      self.root_node_name = self.get_root_node_name()
    else:
      self.content_dom = None
      self.root_node_name = None

    self.transformed_doc = None
    self.transformed_dom = None

    # SZ: This should be abstracted out
    self.doctype        = None
    self.doc_schema     = None
    self.doc_class_rel  = DOC_CLASS_REL

  def process(self):
    if not self.is_binary:
      self.f_objs_str = 'f_objs'
      p = self._process()
      if p and p.has_key(self.f_objs_str):
        self.f_objs = p[self.f_objs_str]

  def get_document_digest(self):
    if self.is_binary:
      return hashlib.sha1(self.content).hexdigest()
    else:
      md = hashlib.sha256()
      md.update(self.content)
      return md.hexdigest()

  def get_document_size(self):
    if self.is_binary:
      file = ContentFile(self.content)
      return file.size
    else:
      return len(self.content)

  def get_stylesheet(self):
    ext = '.xsl'
    if settings.XSLT_STYLESHEET_LOC:
      # get the path to the stylesheet from DOC_CLASS_REL mapping above
      doc_type_info = self.doc_class_rel[self.get_type()]
      if doc_type_info.has_key('stylesheet'):
        stylesheet_path = "%s%s%s" % (settings.XSLT_STYLESHEET_LOC, doc_type_info['stylesheet'], ext)
        if os.path.exists(stylesheet_path):
          return open(stylesheet_path).read()

    return None

  def get_schema_file(self):
    ext = '.xsd'
    if self.get_type() and settings.XSD_SCHEMA_LOC:
      doc_type_info = self.doc_class_rel[self.get_type()]
      if doc_type_info.has_key('schema'):
        schema_path = "%s%s%s"%(settings.XSD_SCHEMA_LOC, doc_type_info['schema'], ext)
        if os.path.exists(schema_path):
          return open(schema_path).read()
        else:
          raise ValueError("BAD SCHEMA PATH: %s"%schema_path)

  def validate_xml_syntax(self, xml_doc):
    ''' Make sure that the incoming document is properly formatted XML, regardless of content'''
    try:
      xml_etree = etree.XML(xml_doc)
    except Exception as e:
      raise ValueError("Input document didn't parse as XML, error was: %s"%(str(e)))

  def validate_xml(self, xml_doc, xsd_doc):
    # the <include /> tags in our xsd files are relative paths from the schema dir,
    # so lxml won't find the referenced files unless we resolve the schemaLocation property.
    # We're only looking at the top level, to avoid slow reparsing the entire document
    schema_etree = etree.XML(xsd_doc)
    for el in schema_etree.iterchildren():
      if hasattr(el.tag, 'endswith') and el.tag.endswith("include"):
        include_file = el.get("schemaLocation")
        # This only works for one-level calls--if there are chained includes, this still fails
        el.set("schemaLocation", "%s%s"%(settings.XSD_SCHEMA_LOC, include_file))

    schema = etree.XMLSchema(schema_etree)
    doc = etree.XML(xml_doc)
    if schema.validate(doc):
      return True
    else:
      raise ValueError("Input document didn't validate, error was: %s"%(schema.error_log.last_error))
    

  def apply_stylesheet(self, xml_doc, xsl_doc):
    try:
      style = etree.XSLT(etree.XML(xsl_doc))
      doc = etree.XML(xml_doc)
      result = style(doc)
      result_str = str(result)

      # Return result
      return result_str
    except:
      return False

  def _process(self):
    """ Process the incoming doc """

    # Is this document registered in document schema?
    # Is this document registered in doc_class_rel?
    # Does doc_class_rel contain 'class'?
    # FIXME: we should stop using this globals() approach. Not good. (Ben)
    doc_schema = self.get_document_schema()
    if  doc_schema and \
        self.doc_class_rel.has_key(doc_schema.type) and \
        globals().has_key(self.doc_class_rel[doc_schema.type]['class']):

      # Validate the document XML
      if settings.VALIDATE_XML:
        schema = self.get_schema_file()
        if schema:
          self.validate_xml(self.content, schema)

      # Get the object that corresponds to the incoming xml node name
      dp_data_obj = globals()[self.doc_class_rel[doc_schema.type]['class']]()

      # Retrieve a stylesheet, if there is one
      stylesheet = self.get_stylesheet()
      if stylesheet:
        self.transformed_doc = self.apply_stylesheet(self.content, stylesheet)
        self.transformed_dom = self.get_dom(self.transformed_doc)

      # Test for a process method
      # If dp_data_obj has a process method then use it
      # else use document_processing standard
      if hasattr(dp_data_obj, DP_DOBJ_PROCESS):
        if self.root_node_name in ('HealthActionPlan', 'HealthActionResult'):
          doc_data = dp_data_obj.process(self.root_node_name, self.transformed_dom, self.content)
        else:
          doc_data = dp_data_obj.process(self.root_node_name, self.transformed_dom)
      else:
        doc_data = self.parse_standard_facts_doc(self.root_node_name, self.transformed_dom)

      # If dp_data_obj has the post_data method
      # then post it and set and return the fact obj
      if hasattr(dp_data_obj, DP_DOBJ_POST_DATA) and doc_data:
        try:
          f_objs = []
          for data in doc_data:
            f_objs.append(dp_data_obj.post_data(**data))
          if f_objs:
            return {self.f_objs_str : f_objs}
        except ValueError, e:
          # FIXME: this rollback here doesn't seem to do the right thing
          # because we're not in a transaction. If we're going to roll
          # back a transaction, it should probably happen at a higher level,
          # probably in the view.
          try:
            transaction.rollback()
          except:
            # no transaction management is fine
            pass

          
          # we raise the exception, if processing fails we need to stop 
          raise e
    return False

  def parse_standard_facts_doc(self, root_node_name, xmldom):
    retval_facts = []

    # if there is a DOM, use etree find
    if xmldom is not None:
      for fact in xmldom.findall('fact'):
        # make a dictionary of the immediate children tags of the fact
        new_fact = dict([(e.tag, e.text) for e in fact.getchildren()])
        retval_facts.append(new_fact)

    if retval_facts:
      return retval_facts
    return False

  def unicode_to_string(self, s):
    retval = s
    if isinstance(s, unicode):
      retval = str(s)
    return retval

  def get_root_node_name(self):
    """
    get the namespace and remove it from the full tag,
    which is formatted as {ns}tag
    """
    if self.content_dom is not None:
      ns = self.get_root_node_ns()
      return self.content_dom.tag.replace("{%s}" % ns, "")

  def get_root_node_ns(self):
    """
    get the URI of the namespace, by mapping the prefix
    with the NS map.
    """
    if self.content_dom is not None:
      nsmap = self.content_dom.nsmap
      if nsmap.has_key(self.content_dom.prefix):
        return nsmap[self.content_dom.prefix]
      else:
        return ""

  def get_type(self):
    if not self.doctype:
      if self.content_dom is not None:
        self.doctype = "%s%s" % (self.get_root_node_ns(), self.get_root_node_name())
    return self.doctype

  def get_document_schema(self):
    if self.is_binary:
      return None
    if not self.doc_schema:
      if self.get_type():
        self.doc_schema, created_p = DocumentSchema.objects.get_or_create(type=self.doctype, 
                                                                          defaults={'internal_p':False})
    return self.doc_schema

  def get_dom(self, doc):
    try:
      return etree.fromstring(doc)
    except:
      return None

  def get_clean_xml(self, doc):
    # SZ: Do more cleaning!
    return doc.strip()
