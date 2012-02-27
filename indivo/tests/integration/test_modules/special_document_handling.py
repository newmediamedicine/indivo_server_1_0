import os
import data

from utils import parse_xml, xpath

PRD = 'prd'

def test_special_document_handling(IndivoClient):
  CONTACT = 'contact'
  DEMOGRAPHICS = 'demographics'

  try:
    admin_client = IndivoClient(data.machine_app_email, data.machine_app_secret)
    record_id = admin_client.create_record(data=data.contact).response[PRD]['Record'][0]
    admin_client.set_app_id(data.app_email)
    admin_client.set_record_owner(data=data.account['account_id'])
  
    chrome_client = IndivoClient('chrome', 'chrome')
    chrome_client.create_session(data.account)
    chrome_client.read_record(record_id=record_id)
    chrome_client.put_special_document(special_document=DEMOGRAPHICS, data=data.demographics)
    chrome_client.read_special_document(special_document=DEMOGRAPHICS)
    chrome_client.put_special_document(special_document=CONTACT, data=data.contact)
    chrome_client.read_special_document(special_document=CONTACT)

    # replace the contact document
    chrome_client.put_special_document(special_document=CONTACT, data=data.contact02)
    record_doc = parse_xml(chrome_client.read_record())

    # make sure the label of the record was updated
    record_label = xpath(record_doc,'/Record/@label')[0]
    contact_fullname = xpath(parse_xml(data.contact02), '/ns:Contact/ns:name/ns:fullName/text()', namespaces={'ns':'http://indivo.org/vocab/xml/documents#'})[0]
    assert record_label == contact_fullname, "record label is %s while contact_fullname is %s" % (record_label, contact_fullname)

  except Exception, e:
    return False, e
  return True

