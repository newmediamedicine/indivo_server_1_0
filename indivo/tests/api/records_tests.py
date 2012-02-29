from indivo.models import *
from indivo.tests.internal_tests import InternalTests, TransactionInternalTests
from indivo.tests.data import *

from django.utils.http import urlencode
from lxml import etree

DOCUMENT_TYPE = 'Lab'
AUDIT_FUNC_NAME = 'record_app_specific_document'
CARENET_LABEL = 'New Carenet'
REL = 'annotation'
STATUS = {'status':'void', 'reason':'because I CAN'}
LAB_CODE = 'HBA1C' # MAKE SURE TO ADD THESE MEASUREMENTS

SHOW_CUSTOM_DOC_REPORTS = False # set to True to display reports for all custom document types

ADHERENCEITEM_DOC1 = """<AdherenceItem xmlns="http://indivo.org/vocab/xml/documents#">
	<name>Atorvastatin 40 MG Oral Tablet [Lipitor]</name>
	<reportedBy>rpoole@records.media.mit.edu</reportedBy>
	<dateReported>2009-05-17T08:52:21-04:00</dateReported>
	<recurrenceIndex>0</recurrenceIndex>
	<adherence>true</adherence>
</AdherenceItem>"""

ADHERENCEITEM_DOC2 = """<AdherenceItem xmlns="http://indivo.org/vocab/xml/documents#">
	<name>Fish Oil Capsules</name>
	<reportedBy>rpoole@records.media.mit.edu</reportedBy>
	<dateReported>2009-05-17T08:52:21-04:00</dateReported>
	<recurrenceIndex>0</recurrenceIndex>
	<adherence>true</adherence>
</AdherenceItem>"""

EQUIPMENTSCHEDULEITEM_DOC = """<EquipmentScheduleItem xmlns="http://indivo.org/vocab/xml/documents#">
	<name> FORA D15b </name>
<scheduledBy>jking@records.media.mit.edu</scheduledBy>
	<dateScheduled>2011-02-14T13:00:00-04:00</dateScheduled>
	<dateStart>2011-02-15T10:00:00-04:00</dateStart>
<dateEnd>2011-02-15T14:00:00-04:00</dateEnd>
	<recurrenceRule>
		<frequency>DAILY</frequency>
		<count>30</count>
	</recurrenceRule>
	<instructions>press the big blue button</instructions>
</EquipmentScheduleItem>"""

MEDICATIONADMINISTRATION_DOC = """<MedicationAdministration xmlns="http://indivo.org/vocab/xml/documents#">
	<name type="http://rxnav.nlm.nih.gov/REST/rxcui/" value="617320">Atorvastatin 40 MG Oral Tablet [Lipitor]</name>
	<reportedBy>rpoole@records.media.mit.edu</reportedBy>
	<dateReported>2009-05-17T08:52:21-04:00</dateReported>
	<dateAdministered>2009-05-17T08:52:21-04:00</dateAdministered>
    <amountAdministered>
        <value>1</value>
        <textValue>placebo</textValue>
	    <unit>tablet</unit>
    </amountAdministered>
    <amountRemaining>
        <value>29</value>
	    <unit>tablet</unit>
    </amountRemaining>
</MedicationAdministration>"""

MEDICATIONFILL_DOC = """<MedicationFill xmlns="http://indivo.org/vocab/xml/documents#">
	<name type="http://rxnav.nlm.nih.gov/REST/rxcui/" value="617320">Atorvastatin 40 MG Oral Tablet [Lipitor]</name>
	<filledBy>pharmacist@records.media.mit.edu</filledBy>
	<dateFilled>2009-05-16T14:02:51-04:00</dateFilled>
	<amountFilled>
		<value>30</value>
        <textValue>placebo</textValue>
		<unit>tablet</unit>
</amountFilled>
	<ndc>65427004730</ndc>
    <fillSequenceNumber>000234587</fillSequenceNumber>
    <lotNumber>0855020</lotNumber>
    <instructions>take with water</instructions>
</MedicationFill>"""

MEDICATIONORDER_DOC = """<MedicationOrder xmlns="http://indivo.org/vocab/xml/documents#">
	<name type="http://rxnav.nlm.nih.gov/REST/rxcui/" value="310798">Hydrochlorothiazide 25 MG Oral Tablet</name>
	<orderType>prescribed</orderType>
	<orderedBy>jking@records.media.mit.edu </orderedBy>
	<dateOrdered>2011-02-14T09:00:00-04:00</dateOrdered>
	<dateExpires>2011-05-14T09:00:00-04:00</dateExpires>
	<indication>hypertension</indication>
	<amountOrdered>
		<value>30</value>
        <textValue>placebo</textValue>
		<unit  type="http://indivo.org/codes/units#" value="tab" abbrev="tab">tablet</unit>
	</amountOrdered>
	<substitutionPermitted>true</substitutionPermitted>
	<instructions>take with water</instructions>
</MedicationOrder>"""

MEDICATIONSCHEDULEITEM_DOC = """<MedicationScheduleItem xmlns="http://indivo.org/vocab/xml/documents#">
	<name type="http://rxnav.nlm.nih.gov/REST/rxcui/" value="617320">Atorvastatin 40 MG Oral Tablet [Lipitor]</name>
<scheduledBy>jking@records.media.mit.edu</scheduledBy>
	<dateScheduled>2011-02-14T13:00:00-04:00</dateScheduled>
	<dateStart>2011-02-15T10:00:00-04:00</dateStart>
<dateEnd>2011-02-15T14:00:00-04:00</dateEnd>
	<recurrenceRule>
		<frequency>DAILY</frequency>
		<count>30</count>
	</recurrenceRule>
	<dose>
		<value>1</value>
        <textValue>placebo</textValue>
		<unit  type="http://indivo.org/codes/units#" value="tab" abbrev="tab">tablet</unit>
	</dose>
	<instructions>take in the evening for maximum benefit</instructions>
</MedicationScheduleItem>"""

VIDEOMESSAGE_DOC = """<VideoMessage xmlns="http://indivo.org/vocab/xml/documents#">
	<fileId>rpoole1</fileId>
	<storageType>FlashMediaServer</storageType>
<subject>Nice Job Robert</subject>
	<from>jking@records.media.mit.edu</from>
	<dateRecorded>2009-05-17T08:52:21-04:00</dateRecorded>
	<dateSent>2009-05-17T08:52:21-04:00</dateSent>
</VideoMessage>"""

VITALS_DOC = """<VitalSign xmlns="http://indivo.org/vocab/xml/documents#">
	<name type="http://codes.indivo.org/vitalsigns/" value="123" abbrev="BPsys">Blood Pressure Systolic</name>
	<measuredBy>rpoole@records.media.mit.edu</measuredBy>
  	<dateMeasuredStart>2009-05-16T15:23:21-04:00</dateMeasuredStart>
  	<result>
  		<value>145</value>
        <textValue>placebo</textValue>
  		<unit type="http://codes.indivo.org/units/" value="31" abbrev="mmHg">millimeters of mercury</unit>
	</result>
  	<site>left arm</site>
  	<position>sitting</position>
</VitalSign>"""

def recordStateSetUp(test_cases_instance):
    _self = test_cases_instance
    super(_self.__class__, _self).setUp()
    
    # reset our state
    _self.ras_docs = []
    _self.rs_docs = []
    
    # Create an Account
    _self.account = _self.createAccount(TEST_ACCOUNTS, 4)
    
    # Create a record for the account
    _self.record = _self.createRecord(TEST_RECORDS, 0, owner=_self.account)

    # Create an App
    _self.pha = _self.createUserApp(TEST_USERAPPS, 0)

    # Add the app to a record
    share_args = {'record': _self.record,
                  'with_pha': _self.pha}
    _self.addAppToRecord(**share_args)

    # Create a record-app-specific doc
    _self.ras_docs.append(_self.createDocument(TEST_RA_DOCS, 0, record=_self.record, pha=_self.pha))

    # Create a record-specific doc
    _self.rs_docs.append(_self.createDocument(TEST_R_DOCS, 6, record = _self.record))

    # Create a record-specific doc with an external id
    _self.rs_docs.append(_self.createDocument(TEST_R_DOCS, 0, record=_self.record))

    # Create a contact and demographics doc
    _self.rs_docs.append(_self.createDocument(TEST_CONTACTS, 0, record=_self.record))

    _self.rs_docs.append(_self.createDocument(TEST_DEMOGRAPHICS, 0, record=_self.record))

    # Set our record's special docs
    _self.record.demographics = _self.rs_docs[3]
    _self.record.contact = _self.rs_docs[2]
    _self.record.save()

    # The message we will send (not yet in the DB)
    _self.message = TEST_MESSAGES[2]

    # An attachment to attach (not yet in the DB)
    _self.attachment = TEST_ATTACHMENTS[0]


class TransactionRecordInternalTests(TransactionInternalTests):

    ras_docs = []
    rs_docs = []

    def setUp(self):
        return recordStateSetUp(self)

    def tearDown(self):
        return super(TransactionRecordInternalTests,self).tearDown()
    
    def test_duplicate_ext_ids(self):

        # Test doc creation w/ duplicate ext_ids
        record_id = self.record.id
        ext_id = TEST_R_DOCS[1]['external_id']
        pha_email = self.pha.email
        url = '/records/%s/documents/external/%s/%s'%(record_id, pha_email, ext_id)
        response = self.client.put(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

        # Try twice with the same ext_id, expect 400
        response = self.client.put(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 400)

        #Test record_send_message w/ duplicate ext_ids
        record_id = self.record.id
        msg = self.message
        data = {'subject':msg['subject'],
                'body':msg['body'],
                'body_type':msg['body_type'],
                'num_attachments':msg['num_attachments'],
                'severity':msg['severity']}

        # Send a message
        url = '/records/%s/inbox/%s'%(record_id, msg['message_id'])
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

        # Attach to the message
        url = '/records/%s/inbox/%s/attachments/%s'%(record_id, msg['message_id'], self.attachment['attachment_num'])
        response = self.client.post(url, data=self.attachment['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

        # Attach again to the same attachment_num, should break
        url = '/records/%s/inbox/%s/attachments/%s'%(record_id, msg['message_id'], self.attachment['attachment_num'])
        response = self.client.post(url, data=self.attachment['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 400)        
        
        # Send message again to the same message_id, should break
        url = '/records/%s/inbox/%s'%(record_id, msg['message_id'])
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 400)


class RecordInternalTests(InternalTests):
    ras_docs = []
    rs_docs = []

    def setUp(self):
        return recordStateSetUp(self)

    def tearDown(self):
        super(RecordInternalTests,self).tearDown()

    def test_create_record_ext(self):
        principal_email = self.account.email
        url='/records/external/%s/%s'%(principal_email, TEST_RECORDS[5]['external_id'])
        response = self.client.put(url, data=TEST_CONTACTS[0]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)
        # Check for label, contact doc, etc.

    def test_create_record(self):
        url = '/records/' 
        response = self.client.post(url, data=TEST_CONTACTS[0]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)
        # Check for label, contact doc, etc.

    def test_list_record_apps(self):
        record_id = self.record.id
        url = '/records/%s/apps/'%(record_id) 
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # Make sure apps are correct!

    def test_get_record_app(self):
        record_id = self.record.id
        pha_email = self.pha.email
        url = '/records/%s/apps/%s'%(record_id, pha_email) 
        bad_methods = ['post',]
        self.check_unsupported_http_methods(bad_methods, url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # Make sure app is correct!

    def test_delete_record_app(self):
        record_id = self.record.id
        pha_email = self.pha.email
        url = '/records/%s/apps/%s'%(record_id, pha_email) 
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)

    def test_enable_record_app(self):
        record_id = self.record.id
        pha_email = self.pha.email
        url = '/records/%s/apps/%s'%(record_id, pha_email) 

        # The app should be enabled by the setup
        self.assertTrue(PHAShare.objects.filter(record__id=record_id, with_pha__email=pha_email).exists())
        
        # The call should work, but do nothing when the share exists
        response = self.client.put(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PHAShare.objects.filter(record__id=record_id, with_pha__email=pha_email).exists())

        # Now, drop the share and assert that it's gone
        PHAShare.objects.get(record__id=record_id, with_pha__email=pha_email).delete()
        self.assertFalse(PHAShare.objects.filter(record__id=record_id, with_pha__email=pha_email).exists())
        
        # Now, make the call again, and expect the share to re-appear
        response = self.client.put(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PHAShare.objects.filter(record__id=record_id, with_pha__email=pha_email).exists())
        
        # the share should be authorized by None (since we authenticated as the NoUser)
        # the share should be authorized recently (i.e. within the last second)
        new_share = PHAShare.objects.get(record__id=record_id, with_pha__email=pha_email)
        self.assertEqual(new_share.authorized_by, None)
        self.assertTimeStampsAlmostEqual(new_share.authorized_at, seconds=1)

    def test_record_app_specific_docs_ext(self):
        # Multiple calls, to avoid having to resolve ext_ids ourselves
        record_id = self.record.id
        pha_email = self.pha.email

        # Create a rec-app specific doc by ext_id, post
        url = '/records/%s/apps/%s/documents/external/%s'%(record_id, pha_email, TEST_RA_DOCS[1]['external_id'])
        response = self.client.post(url, data=TEST_RA_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)
        
        # Create by put (should overwrite doc)
        url = '/records/%s/apps/%s/documents/external/%s'%(record_id, pha_email, TEST_RA_DOCS[1]['external_id'])
        response = self.client.put(url, data=TEST_RA_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

        # Get Meta by ext_id
        url = '/records/%s/apps/%s/documents/external/%s/meta'%(record_id, pha_email, TEST_RA_DOCS[1]['external_id']) 
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # Check for correctness

    def test_get_record_app_specific_doc(self):
        record_id = self.record.id
        pha_email = self.pha.email
        doc_id = self.ras_docs[0].id
        url = '/records/%s/apps/%s/documents/%s'%(record_id, pha_email, doc_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # Check that we got the doc

    def test_delete_record_app_specific_doc(self):
        record_id = self.record.id
        pha_email = self.pha.email
        doc_id = self.ras_docs[0].id
        url = '/records/%s/apps/%s/documents/%s'%(record_id, pha_email, doc_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)

    def test_set_record_app_specific_doc_label(self):
        record_id = self.record.id
        pha_email = self.pha.email
        doc_id = self.ras_docs[0].id
        url = '/records/%s/apps/%s/documents/%s/label'%(record_id, pha_email, doc_id)
        bad_methods = ['get', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.put(url, data=TEST_RA_DOCS[0]['label'], content_type='text/plain')
        self.assertEquals(response.status_code, 200)

    def test_get_record_app_specific_doc_meta(self):
        record_id = self.record.id
        pha_email = self.pha.email
        doc_id = self.ras_docs[0].id
        url = '/records/%s/apps/%s/documents/%s/meta'%(record_id, pha_email, doc_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_list_record_app_specific_docs(self):
        record_id = self.record.id
        pha_email = self.pha.email
        url = '/records/%s/apps/%s/documents/'%(record_id, pha_email)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_create_record_app_specific_doc(self):
        record_id = self.record.id
        pha_email = self.pha.email
        url = '/records/%s/apps/%s/documents/'%(record_id, pha_email)
        response = self.client.post(url, data=TEST_RA_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

    def test_setup_record_app(self):
        record_id = self.record.id
        pha_email = self.pha.email
        url = '/records/%s/apps/%s/setup'%(record_id, pha_email)
        bad_methods = ['get', 'put', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.post(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)
    
    def test_get_view_function_audit(self):
        # Need to Create Audit Logs
        record_id = self.record.id
        doc_id = self.ras_docs[0].id
        func_name = AUDIT_FUNC_NAME
        url = '/records/%s/audits/documents/%s/functions/%s/'%(record_id, doc_id, func_name)
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_document_audit(self):
        # Need to Create Audit logs
        record_id = self.record.id
        doc_id = self.ras_docs[0].id
        url = '/records/%s/audits/documents/%s/'%(record_id, doc_id)
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_record_audit(self):
        # Need to create Audit logs
        record_id = self.record.id
        url = '/records/%s/audits/'%(record_id)
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_record_audit_query(self):
        # Need to create Audit logs
        record_id = self.record.id
        doc_id = self.ras_docs[0].id
        url = '/records/%s/audits/query/?document_id=%s'%(record_id, doc_id)
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_list_all_autoshares(self):
        # Need to create autoshares
        record_id = self.record.id
        url='/records/%s/autoshare/bytype/all'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_list_autoshares_by_type(self):
        #Need to create autoshares
        record_id = self.record.id
        type = DOCUMENT_TYPE
        url = '/records/%s/autoshare/bytype/'%(record_id)
        response = self.client.get(url, data={'type': type})
        self.assertEquals(response.status_code, 200)

    def test_autoshare_create(self):
        record_id = self.record.id
        data = {'type': DOCUMENT_TYPE}
        carenet_id = Carenet.objects.filter(record = self.record)[0].id
        url = '/records/%s/autoshare/carenets/%s/bytype/set'%(record_id, carenet_id)
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_autoshare_delete(self):
        record_id = self.record.id
        data = {'type': DOCUMENT_TYPE}
        carenet_id = Carenet.objects.filter(record = self.record)[0].id
        url = '/records/%s/autoshare/carenets/%s/bytype/unset'%(record_id, carenet_id)
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)
        # CREATE AUTOSHARE TO DELETE

    def test_list_record_carenets(self):
        record_id = self.record.id
        url = '/records/%s/carenets/'%(record_id) 
        response =self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_create_record_carenet(self):
        record_id = self.record.id
        url = '/records/%s/carenets/'%(record_id)
        data = {'name': CARENET_LABEL}
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_set_record_specific_doc_label_ext(self):
        record_id = self.record.id
        ext_id = TEST_R_DOCS[0]['external_id']
        pha_email = self.pha.email
        bad_methods = ['get', 'post', 'delete']
        url= '/records/%s/documents/external/%s/%s/label'%(record_id, pha_email, ext_id)
        self.check_unsupported_http_methods(bad_methods, url)
        response = self.client.put(url, data=TEST_R_DOCS[0]['label'], content_type='text/plain')
        self.assertEquals(response.status_code, 200)

    def test_get_record_specific_doc_meta_ext(self):
        record_id = self.record.id
        ext_id = TEST_R_DOCS[0]['external_id']
        pha_email = self.pha.email
        url = '/records/%s/documents/external/%s/%s/meta'%(record_id, pha_email, ext_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_create_record_specific_doc_ext(self):
        record_id = self.record.id
        ext_id = TEST_R_DOCS[1]['external_id']
        pha_email = self.pha.email
        url = '/records/%s/documents/external/%s/%s'%(record_id, pha_email, ext_id)
        response = self.client.put(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

    def test_relate_existing_record_specific_docs(self):
        record_id = self.record.id
        rel = REL
        doc_id_0 = self.rs_docs[0].id
        doc_id_1 = self.rs_docs[1].id
        url = '/records/%s/documents/%s/rels/%s/%s'%(record_id, doc_id_0, rel, doc_id_1)
        response = self.client.put(url)
        self.assertEquals(response.status_code, 200)

    def test_create_record_specific_doc_by_rel_ext(self):
        record_id = self.record.id
        ext_id = TEST_R_DOCS[1]['external_id']
        rel = REL
        pha_email = self.pha.email
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/rels/%s/external/%s/%s'%(record_id, doc_id, rel, pha_email, ext_id)
        response = self.client.post(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

        # Test put as well, should create new doc
        ext_id = TEST_R_DOCS[2]['external_id']
        url = '/records/%s/documents/%s/rels/%s/external/%s/%s'%(record_id, doc_id, rel, pha_email, ext_id)
        response = self.client.put(url, data=TEST_R_DOCS[2]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

    def test_get_record_specific_docs_by_rel(self):
        record_id = self.record.id
        rel = REL
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/rels/%s/'%(record_id, doc_id, rel)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # CREATE RELS TO LOOK UP

    def test_create_record_specific_doc_by_rel(self):
        record_id = self.record.id
        rel = REL
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/rels/%s/'%(record_id, doc_id, rel)
        response = self.client.post(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)
        
    def test_get_record_specific_doc_carenets(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/carenets/'%(record_id, doc_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # PLACE DOC IN CARENETS

    def test_revert_record_specific_doc_autoshare(self):
        # NOT YET IMPLEMENTED!!        
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        carenet_id = Carenet.objects.filter(record = self.record)[0].id
        url = '/records/%s/documents/%s/carenets/%s/autoshare-revert'%(record_id, doc_id, carenet_id)
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)

    def test_place_record_specific_doc_in_carenet(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        carenet_id = Carenet.objects.filter(record = self.record)[0].id
        url = '/records/%s/documents/%s/carenets/%s'%(record_id, doc_id, carenet_id)
        response = self.client.put(url)
        self.assertEquals(response.status_code, 200)

    def test_remove_record_specific_doc_from_carenet(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        carenet_id = Carenet.objects.filter(record = self.record)[0].id
        url = '/records/%s/documents/%s/carenets/%s'%(record_id, doc_id, carenet_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)
        # CODE LOOKS FUNKY--MAKE SURE THIS WORKS FOR REAL

    def test_get_record_specific_doc(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s'%(record_id, doc_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_set_record_specific_doc_label(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/label'%(record_id, doc_id)
        bad_methods = ['get', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)
        response = self.client.put(url, data=TEST_R_DOCS[1]['label'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)
        
    def test_get_record_specific_doc_meta(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/meta'%(record_id, doc_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        # Make sure metadata fields worked correctly
        xml = etree.XML(response.content)

        created_at = xml.findtext('createdAt')
        self.assertNotRaises(ValueError, self.validateIso8601, created_at)

        creator_name = xml.find('creator').findtext('fullname')
        self.assertEqual(creator_name, self.rs_docs[0].creator.descriptor())

        # TODO: Check remaining fields

    def test_update_record_specific_doc_meta(self):
        # Call does nothing.
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/meta'%(record_id, doc_id)
        response = self.client.put(url)
        self.assertEquals(response.status_code, 200)
        
    def test_set_record_specific_doc_nevershare(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/nevershare'%(record_id, doc_id)
        response = self.client.put(url)
        self.assertEquals(response.status_code, 200)
        
    def test_remove_record_specific_doc_nevershare(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/nevershare'%(record_id, doc_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)
        # ADD NEVERSHARE TO REMOVE

    def test_replace_record_specific_doc_ext(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        pha_email = self.pha.email
        ext_id = TEST_R_DOCS[1]['external_id']
        url = '/records/%s/documents/%s/replace/external/%s/%s'%(record_id, doc_id, pha_email, ext_id)
        response = self.client.put(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

    def test_replace_record_specific_doc(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/replace'%(record_id, doc_id)
        response = self.client.post(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)
        
    def test_set_record_specific_doc_status(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/set-status'%(record_id, doc_id)
        response = self.client.post(url, data=urlencode(STATUS), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_get_record_specific_doc_status_history(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/status-history'%(record_id, doc_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # CREATE STATUS HISTORY ON DOC

    def test_get_record_specific_doc_versions(self):
        record_id = self.record.id
        doc_id = self.rs_docs[0].id
        url = '/records/%s/documents/%s/versions/'%(record_id, doc_id)
        bad_methods = ['put', 'post', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # CREATE VERSIONS ON DOC

    def test_list_record_specific_docs(self):
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_create_record_specific_doc(self):
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.post(url, data=TEST_R_DOCS[1]['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

    def test_delete_all_record_specific_docs(self):
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)

    def test_get_special_doc(self):
        record_id = self.record.id
        for doc_type in SPECIAL_DOCS.keys():
            url = '/records/%s/documents/special/%s'%(record_id, doc_type)
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)

    def test_set_special_doc(self):
        record_id = self.record.id
        for doc_type, doc in SPECIAL_DOCS.iteritems():
            url = '/records/%s/documents/special/%s'%(record_id, doc_type)
            
            # post
            response = self.client.post(url, data=doc, content_type='text/xml')
            self.assertEquals(response.status_code, 200)

            # put, should have same behavior
            response = self.client.post(url, data=doc, content_type='text/xml')
            self.assertEquals(response.status_code, 200)

    def test_get_record_info(self):
        record_id = self.record.id
        url = '/records/%s'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_record_send_message(self):
        # Test send and attach together to avoid setup
        record_id = self.record.id
        msg = self.message
        data = {'subject':msg['subject'],
                'body':msg['body'],
                'body_type':msg['body_type'],
                'num_attachments':msg['num_attachments'],
                'severity':msg['severity']}

        # Send a message
        url = '/records/%s/inbox/%s'%(record_id, msg['message_id'])
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)
        
        # Attach to the message
        url = '/records/%s/inbox/%s/attachments/%s'%(record_id, msg['message_id'], self.attachment['attachment_num'])
        response = self.client.post(url, data=self.attachment['content'], content_type='text/xml')
        self.assertEquals(response.status_code, 200)

    def test_record_notify(self):
        record_id = self.record.id

        # Test Deprecated Call
        url = '/records/%s/notify'%(record_id)
        bad_methods = ['get', 'put', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        data = {'content':TEST_R_DOCS[1]['content'],
                'document_id':self.rs_docs[1].id}
        response =self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

        # Test Modern Call
        url = '/records/%s/notifications/'%(record_id)
        bad_methods = ['get', 'put', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        data = {'content':TEST_R_DOCS[1]['content'],
                'document_id':self.rs_docs[1].id}
        response =self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_get_record_owner(self):
        record_id = self.record.id
        url = '/records/%s/owner'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_set_record_owner(self):
        record_id = self.record.id
        url = '/records/%s/owner'%(record_id)
        response = self.client.post(url, data=self.pha.email, content_type='text/plain')
        self.assertEquals(response.status_code, 200)
        
        # Test put: should have same behavior
        response = self.client.put(url, data=self.pha.email, content_type='text/plain')
        self.assertEquals(response.status_code, 200)

    def test_reset_record_password(self):
        # records/%s/password_reset ['GET'] 
        # DOES NOTHING... Why does this call exist?
        pass

    def test_get_record_shares(self):
        record_id = self.record.id
        url = '/records/%s/shares/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # CREATE SHARES
        
    def test_add_record_share(self):
        record_id = self.record.id
        url = '/records/%s/shares/'%(record_id)
        data = {'account_id':self.account.email,
                'role_label':'NEW OWNER'}
        response = self.client.post(url, data=urlencode(data), content_type='application/x-www-form-urlencoded')
        self.assertEquals(response.status_code, 200)

    def test_remove_record_share(self):
        record_id = self.record.id
        other_account_id = self.account.email

        # Test deprecated call
        url = '/records/%s/shares/%s/delete'%(record_id, other_account_id)

        bad_methods = ['get', 'put', 'delete']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)

        # Test modern call
        url = '/records/%s/shares/%s'%(record_id, other_account_id)

        bad_methods = ['get', 'put', 'post']
        self.check_unsupported_http_methods(bad_methods, url)

        response = self.client.delete(url)
        self.assertEquals(response.status_code, 200)

        # CREATE SHARES

    def test_get_record_ccr(self):
        record_id = self.record.id
        url = '/records/%s/reports/experimental/ccr'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_allergies(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/allergies/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_equipment(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/equipment/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_immunizations(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/immunizations/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_labs(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/labs/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_measurements(self):
        record_id = self.record.id
        lab_code = LAB_CODE
        url = '/records/%s/reports/minimal/measurements/%s/'%(record_id, lab_code)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_medications(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/medications/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_problems(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/problems/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_procedures(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/procedures/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_simple_clinical_notes(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/simple-clinical-notes/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_vitals(self):
        record_id = self.record.id
        url = '/records/%s/reports/minimal/vitals/'%(record_id)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # ADD REPORTS

    def test_get_record_vitals_by_category(self):
        # NOT IMPLEMENTED YET
        pass

    ####################################################
    # now come the tests for the custom document types #
    ####################################################

    def test_adherenceitem(self):
        # create a document
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.post(url, data=ADHERENCEITEM_DOC1, content_type='text/xml')
        #print response.content
        self.assertEquals(response.status_code, 200)

        # get a report containing the document above
        url = '/records/%s/reports/minimal/adherenceitems/'%(record_id)
        response = self.client.get(url)
        if SHOW_CUSTOM_DOC_REPORTS:
            print response.content
        self.assertEquals(response.status_code, 200)

    def test_equipmentscheduleitem(self):
        """ This unit test also tests document relationships """
        #
        # create the EquipmentScheduleItem document
        #
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.post(url, data=EQUIPMENTSCHEDULEITEM_DOC, content_type='text/xml')
        #print response.content
        esi_doc_id = response.content[14:50]
        #print esi_doc_id
        self.assertEquals(response.status_code, 200)

        #
        # now create 2 AdherenceItem documents
        #
        url = '/records/%s/documents/'%(record_id)
        response = self.client.post(url, data=ADHERENCEITEM_DOC1, content_type='text/xml')
        #print response.content
        ai_doc_id_1 = response.content[14:50]
        #print ai_doc_id_1
        self.assertEquals(response.status_code, 200)

        url = '/records/%s/documents/'%(record_id)
        response = self.client.post(url, data=ADHERENCEITEM_DOC2, content_type='text/xml')
        #print response.content
        ai_doc_id_2 = response.content[14:50]
        #print ai_doc_id_2
        self.assertEquals(response.status_code, 200)

        #
        # now relate the AdherenceItem documents created above with the EquipmentScheduleItem document
        #
        rel = "annotation"

        url = '/records/%s/documents/%s/rels/%s/%s'%(record_id, esi_doc_id, rel, ai_doc_id_1)
        response = self.client.put(url)
        #print response.content
        self.assertEquals(response.status_code, 200)

        url = '/records/%s/documents/%s/rels/%s/%s'%(record_id, esi_doc_id, rel, ai_doc_id_2)
        response = self.client.put(url)
        #print response.content
        self.assertEquals(response.status_code, 200)

        #
        # create a Vitals document to relate EquipmentScheduleItem to
        #
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.post(url, data=VITALS_DOC, content_type='text/xml')
        #print response.content
        v_doc_id = response.content[14:50]
        #print v_doc_id
        self.assertEquals(response.status_code, 200)

        rel = "followup"

        url = '/records/%s/documents/%s/rels/%s/%s'%(record_id, v_doc_id, rel, esi_doc_id)
        response = self.client.put(url)
        #print response.content
        self.assertEquals(response.status_code, 200)

        #
        # finally get a report containing the EquipmentScheduleItem document and relating documents
        #
        url = '/records/%s/reports/minimal/equipmentscheduleitems/'%(record_id)
        response = self.client.get(url)
        if SHOW_CUSTOM_DOC_REPORTS:
            print response.content
        self.assertEquals(response.status_code, 200)

    def test_medicationadministration(self):
        # create a document
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.post(url, data=MEDICATIONADMINISTRATION_DOC, content_type='text/xml')
        #print response.content
        self.assertEquals(response.status_code, 200)

        # get a report containing the document above
        url = '/records/%s/reports/minimal/medicationadministrations/'%(record_id)
        response = self.client.get(url)
        if SHOW_CUSTOM_DOC_REPORTS:
            print response.content
        self.assertEquals(response.status_code, 200)

    def test_medicationfill(self):
        # create a document
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.post(url, data=MEDICATIONFILL_DOC, content_type='text/xml')
        #print response.content
        self.assertEquals(response.status_code, 200)

        # get a report containing the document above
        url = '/records/%s/reports/minimal/medicationfills/'%(record_id)
        response = self.client.get(url)
        if SHOW_CUSTOM_DOC_REPORTS:
            print response.content
        self.assertEquals(response.status_code, 200)

    def test_medicationorder(self):
        # create a document
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.post(url, data=MEDICATIONORDER_DOC, content_type='text/xml')
        #print response.content
        self.assertEquals(response.status_code, 200)

        # get a report containing the document above
        url = '/records/%s/reports/minimal/medicationorders/'%(record_id)
        response = self.client.get(url)
        if SHOW_CUSTOM_DOC_REPORTS:
            print response.content
        self.assertEquals(response.status_code, 200)

    def test_medicationscheduleitem(self):
        # create a document
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.post(url, data=MEDICATIONSCHEDULEITEM_DOC, content_type='text/xml')
        #print response.content
        self.assertEquals(response.status_code, 200)

        # get a report containing the document above
        url = '/records/%s/reports/minimal/medicationscheduleitems/'%(record_id)
        response = self.client.get(url)
        if SHOW_CUSTOM_DOC_REPORTS:
            print response.content
        self.assertEquals(response.status_code, 200)

    def test_videomessage(self):
        # create a document
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.post(url, data=VIDEOMESSAGE_DOC, content_type='text/xml')
        #print response.content
        self.assertEquals(response.status_code, 200)

        # get a report containing the document above
        url = '/records/%s/reports/minimal/videomessages/'%(record_id)
        response = self.client.get(url)
        if SHOW_CUSTOM_DOC_REPORTS:
            print response.content
        self.assertEquals(response.status_code, 200)

    def test_vitals(self):
        # create a document
        record_id = self.record.id
        url = '/records/%s/documents/'%(record_id)
        response = self.client.post(url, data=VITALS_DOC, content_type='text/xml')
        #print response.content
        self.assertEquals(response.status_code, 200)

        # get a report containing the document above
        url = '/records/%s/reports/minimal/vitals/'%(record_id)
        response = self.client.get(url)
        if SHOW_CUSTOM_DOC_REPORTS:
            print response.content
        self.assertEquals(response.status_code, 200)
