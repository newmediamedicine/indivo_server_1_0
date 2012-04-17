from indivo.lib import iso8601
from indivo.models import HealthActionResult
from indivo.models import ActionResults
from indivo.models import StopConditionResults
from indivo.models import Occurrences
from indivo.models import Measurements
from indivo.models import DeviceResults
from indivo.models import MedicationAdministrations
from lxml import etree
from StringIO import StringIO

class IDP_HealthActionResult:

    def process(self, root_node_name, xmldom, original_xml):
        """
        moving this to etree
        """
        retval_facts = []

        hap = etree.XML(original_xml)
        actions_element = hap.find('{http://indivo.org/vocab/xml/documents#}actions')

        # if there is a DOM, use etree find
        if xmldom is not None:
            for fact in xmldom.findall('fact'):
                # make a dictionary of the immediate children tags of the fact
                new_fact = dict([(e.tag, e.text) for e in fact.getchildren()])
                new_fact['actions'] = etree.tostring(fact.find('actions'))
                actions_xml = etree.tostring(actions_element).split('\n')
                clean_actions_xml = [tag.strip() for tag in actions_xml]
                clean_actions_xml[0] = '<actions>'
                new_fact['actions_xml'] = ''.join(clean_actions_xml)
                new_fact['actions_xml'] = new_fact['actions_xml'].replace('<action xsi:type="ActionGroupResult">', '<action type="ActionGroupResult">')
                new_fact['actions_xml'] = new_fact['actions_xml'].replace('<action xsi:type="ActionStepResult">', '<action type="ActionStepResult">')
                retval_facts.append(new_fact)

        if retval_facts:
            return retval_facts
        return False

    def post_data(self, name=None,
                        name_type=None,
                        name_value=None,
                        name_abbrev=None,
                        planType=None,
                        reportedBy=None,
                        dateReported=None,
                        actions=None,
                        actions_xml=None):
        OCCURRENCE_TEST = False
        try:
            #
            # The first thing to do is to save just the HealthActionPlan record
            #

            # Convert datetime field
            if dateReported: dateReported = iso8601.parse_date(dateReported)
 
            healthactionresult_obj = HealthActionResult.objects.create(name=name,
                                                                     name_type=name_type,
                                                                     name_value=name_value,
                                                                     name_abbrev=name_abbrev,
                                                                     planType=planType,
                                                                     reportedBy=reportedBy,
                                                                     dateReported=dateReported,
                                                                     actions=actions_xml)

            #
            # With the healthactionresult_obj, take the value of the "id" field
            # and store it in each action record's healthactionresult_id field
            #


            #import pdb; pdb.set_trace()
            #root = etree.XML(actions_xml)
            #print etree.tostring(root, pretty_print=True, method="xml")
            context = etree.iterparse(StringIO(actions), events=("start", "end"))

            occurrence = {}
            measurement = {}
            deviceResult = {}
            medicationAdministration = {}
            occurrence_stopCondition = {}
            occurrence_measurement = {}
            occurrence_deviceResult = {}
            occurrence_medicationAdministration = {}
            groupresult = {}
            stepresult = {}
            action_type = ''

            parent_tag = []

            action_obj = None


            #import pdb; pdb.set_trace()
            for action, elem in context:
                #print("%s: %s :%s" % (action, elem.tag, elem.text))
                if elem.tag in ("actions", "occurrences", "measurements", "deviceResults", "medicationAdministrations"):
                    # I don't care about these tags
                    continue

                if action == "start":
                    #if elem.tag == "ActionStepResult":
                    if elem.tag in ("ActionGroupResult", "ActionStepResult"):
                        #print "Start ", elem.tag
                        if action_type == "ActionGroupResult":
                            #print "Start ", elem.tag

                            #
                            # For every action record stored, use the id attribute of action_obj
                            # and store it in the action_id field of the following tables
                            #
                            action_obj = ActionResults.objects.create(action_type='ActionGroupResult',
                                                   state='Start',
                                                   healthactionresult_id=healthactionresult_obj.id,
                                                   name=groupresult.get('name', None),
                                                   name_type=groupresult.get('name_type', None),
                                                   name_value=groupresult.get('name_value', None),
                                                   name_abbrev=groupresult.get('name_abbrev', None))

                            if groupresult.has_key('measurements'):
                                for a_measurement in groupresult['measurements']:
                                    Measurements.objects.create(action_id=action_obj.id,
                                                                occurrence_id=None,
                                                                name=a_measurement.get('name', None),
                                                                name_type=a_measurement.get('name_type', None),
                                                                name_value=a_measurement.get('name_value', None),
                                                                name_abbrev=a_measurement.get('name_abbrev', None),
                                                                type=a_measurement.get('type', None),
                                                                type_type=a_measurement.get('type_type', None),
                                                                type_value=a_measurement.get('type_value', None),
                                                                type_abbrev=a_measurement.get('type_abbrev', None),
                                                                value_textvalue=a_measurement.get('value_textvalue', None),
                                                                value_value=a_measurement.get('value_value', None),
                                                                value_unit=a_measurement.get('value_unit', None),
                                                                value_unit_type=a_measurement.get('value_unit_type', None),
                                                                value_unit_value=a_measurement.get('value_unit_value', None),
                                                                value_unit_abbrev=a_measurement.get('value_unit_abbrev', None),
                                                                aggregationFunction=a_measurement.get('aggregationFunction', None),
                                                                aggregationFunction_type=a_measurement.get('aggregationFunction_type', None),
                                                                aggregationFunction_value=a_measurement.get('aggregationFunction_value', None),
                                                                aggregationFunction_abbrev=a_measurement.get('aggregationFunction_abbrev', None))

                            if groupresult.has_key('deviceResults'):
                                for a_devicePlan in groupresult['deviceResults']:
                                    DeviceResults.objects.create(action_id=action_obj.id,
                                                                 occurrence_id=None,
                                                                 name=a_devicePlan.get('name', None),
                                                                 name_type=a_devicePlan.get('name_type', None),
                                                                 name_value=a_devicePlan.get('name_value', None),
                                                                 name_abbrev=a_devicePlan.get('name_abbrev', None),
                                                                 type=a_devicePlan.get('type', None),
                                                                 type_type=a_devicePlan.get('type_type', None),
                                                                 type_value=a_devicePlan.get('type_value', None),
                                                                 type_abbrev=a_devicePlan.get('type_abbrev', None),
                                                                 value_textvalue=a_devicePlan.get('value_textvalue', None),
                                                                 value_value=a_devicePlan.get('value_value', None),
                                                                 value_unit=a_devicePlan.get('value_unit', None),
                                                                 value_unit_type=a_devicePlan.get('value_unit_type', None),
                                                                 value_unit_value=a_devicePlan.get('value_unit_value', None),
                                                                 value_unit_abbrev=a_devicePlan.get('value_unit_abbrev', None),
                                                                 site=a_devicePlan.get('site', None),
                                                                 site_type=a_devicePlan.get('site_type', None),
                                                                 site_value=a_devicePlan.get('site_value', None),
                                                                 site_abbrev=a_devicePlan.get('site_abbrev', None))

                            if groupresult.has_key('medicationAdministrations'):
                                for a_medicationAdministration in groupresult['medicationAdministrations']:
                                    MedicationAdministrations.objects.create(action_id=action_obj.id,
                                                                             occurrence_id=None,
                                                                             name=a_medicationAdministration.get('name', None),
                                                                             name_type=a_medicationAdministration.get('name_type', None),
                                                                             name_value=a_medicationAdministration.get('name_value', None),
                                                                             name_abbrev=a_medicationAdministration.get('name_abbrev', None),
                                                                             dose=a_medicationAdministration.get('dose', None),
                                                                             dose_type=a_medicationAdministration.get('dose_type', None),
                                                                             dose_value=a_medicationAdministration.get('dose_value', None),
                                                                             dose_abbrev=a_medicationAdministration.get('dose_abbrev', None),
                                                                             route_textvalue=a_medicationAdministration.get('route_textvalue', None),
                                                                             route_value=a_medicationAdministration.get('route_value', None),
                                                                             route_unit=a_medicationAdministration.get('route_unit', None),
                                                                             route_unit_type=a_medicationAdministration.get('route_unit_type', None),
                                                                             route_unit_value=a_medicationAdministration.get('route_unit_value', None),
                                                                             route_unit_abbrev=a_medicationAdministration.get('route_unit_abbrev', None))

                            #
                            # Prepare the following lists for the next ActionGroupResult tag
                            #
                            groupresult['measurements'] = []
                            groupresult['deviceResults'] = []
                            groupresult['medicationAdministrations'] = []
                        
                        if elem.tag == "ActionGroupResult":
                            #
                            # Make preparations for another ActionGroupResult element
                            #
                            action_type = 'ActionGroupResult'
                            groupresult = {"action_type" : "ActionGroupResult"}
                            groupresult['state'] = 'start'
                            groupresult['repeatCount'] = None
                            parent_tag.insert(0, elem.tag)

                        if elem.tag == 'ActionStepResult':
                            #
                            # Make preparations for another ActionGroupResult element
                            #
                            action_type = 'ActionStepResult'
                            stepresult = {"action_type" : "ActionStepResult"}
                            stepresult['state'] = 'start'
                            stepresult['name'] = None
                            stepresult['name_type'] = None
                            stepresult['name_value'] = None
                            stepresult['name_abbrev'] = None
                            stepresult['type'] = None
                            stepresult['type_type'] = None
                            stepresult['type_value'] = None
                            stepresult['type_abbrev'] = None
                            stepresult['additionalDetails'] = None
                            stepresult['instructions'] = None
                            parent_tag.insert(0, elem.tag)
                        
                        continue

                    if elem.tag in ("occurrence", "stopCondition", "measurement", "deviceResult", "medicationAdministration"):
                        parent_tag.insert(0, elem.tag)
                        continue

                    #if len(parent_tag) == 0: continue
                    if parent_tag[0] in ("occurrence", "stopCondition", "measurement", "deviceResult", "medicationAdministration"):
                        #print parent_tag[0], ' : ', elem.tag, ' : ', elem.text
                        if parent_tag[0] == "occurrence":
                            occurrence[elem.tag] = elem.text
                            OCCURRENCE_TEST = True
                            continue
                        if parent_tag[0] == "stopCondition":
                            if OCCURRENCE_TEST:
                                occurrence_stopCondition[elem.tag] = elem.text
                            else:
                                continue
                        if parent_tag[0] == "measurement":
                            if OCCURRENCE_TEST:
                                occurrence_measurement[elem.tag] = elem.text
                            else:
                                measurement[elem.tag] = elem.text
                            continue
                        if parent_tag[0] == "deviceResult":
                            if OCCURRENCE_TEST:
                                occurrence_deviceResult[elem.tag] = elem.text
                            else:
                                deviceResult[elem.tag] = elem.text
                            continue
                        if parent_tag[0] == "medicationAdministration":
                            if OCCURRENCE_TEST:
                                occurrence_medicationAdministration[elem.tag] = elem.text
                            else:
                                medicationAdministration[elem.tag] = elem.text
                            continue

                    if parent_tag[0] == 'ActionGroupResult':
                        groupresult[elem.tag] = elem.text
                    if parent_tag[0] == 'ActionStepResult':
                        stepresult[elem.tag] = elem.text


                if action == "end":
                    if elem.tag in ("occurrence", "stopCondition", "measurement", "deviceResult", "medicationAdministration"):
                        #print "***GROUP*****"
                        #pprint.pprint(groupresult)
                        #print "------STEP---"
                        #pprint.pprint(stepresult)
                        #print parent_tag[0], ' : ', elem.tag, ' : ', elem.text
                        if elem.tag == "occurrence" and len(occurrence) > 0: # <== This test may have to change...
                            OCCURRENCE_TEST = False
                            if action_type == 'ActionStepResult':
                                if stepresult.has_key('occurrences'):
                                    stepresult['occurrences'].append(occurrence)
                                else:
                                    stepresult['occurrences'] = [occurrence,]
                                occurrence = {}
                        if elem.tag == "stopCondition" and len(occurrence_stopCondition) > 0:
                            if action_type == 'ActionStepResult':
                                if OCCURRENCE_TEST:
                                    if stepresult.has_key('occurrence_stopCondition'):
                                        stepresult['occurrence_stopCondition'].append(occurrence_stopCondition)
                                    else:
                                        stepresult['occurrence_stopCondition'] = [occurrence_stopCondition,]
                                    occurrence_stopCondition = {}
                        if elem.tag == "measurement" and (len(measurement) > 0 or len(occurrence_measurement) > 0):
                            if action_type == 'ActionGroupResult':
                                if groupresult.has_key('measurements'):
                                    groupresult['measurements'].append(measurement)
                                else:
                                    groupresult['measurements'] = [measurement,]
                                measurement = {}
                            else:
                                if OCCURRENCE_TEST:
                                    if stepresult.has_key('occurrence_measurements'):
                                        stepresult['occurrence_measurements'].append(occurrence_measurement)
                                    else:
                                        stepresult['occurrence_measurements'] = [occurrence_measurement,]
                                    occurrence_measurement = {}
                                else:
                                    if stepresult.has_key('measurements'):
                                        stepresult['measurements'].append(measurement)
                                    else:
                                        stepresult['measurements'] = [measurement,]
                                    measurement = {}
                        if elem.tag == "deviceResult" and (len(deviceResult) > 0 or len(occurrence_deviceResult) > 0):
                            if action_type == 'ActionGroupResult':
                                if groupresult.has_key('deviceResults'):
                                    groupresult['deviceResults'].append(deviceResult)
                                else:
                                    groupresult['deviceResults'] = [deviceResult,]
                                deviceResult = {}
                            else:
                                if OCCURRENCE_TEST:
                                    if stepresult.has_key('occurrence_deviceResults'):
                                        stepresult['occurrence_deviceResults'].append(occurrence_deviceResult)
                                    else:
                                        stepresult['occurrence_deviceResults'] = [occurrence_deviceResult,]
                                    occurrence_deviceResult = {}
                                else:
                                    if stepresult.has_key('deviceResults'):
                                        stepresult['deviceResults'].append(deviceResult)
                                    else:
                                        stepresult['deviceResults'] = [deviceResult,]
                                    deviceResult = {}
                        if elem.tag == "medicationAdministration" and \
                                (len(medicationAdministration) > 0 or len(occurrence_medicationAdministration) > 0):
                            if action_type == 'ActionGroupResult':
                                if groupresult.has_key('medicationAdministrations'):
                                    groupresult['medicationAdministrations'].append(medicationAdministration)
                                else:
                                    groupresult['medicationAdministrations'] = [medicationAdministration,]
                                medicationAdministration = {}
                            else:
                                if OCCURRENCE_TEST:
                                    if stepresult.has_key('occurrence_medicationAdministrations'):
                                        stepresult['occurrence_medicationAdministrations'].append(occurrence_medicationAdministration)
                                    else:
                                        stepresult['occurrence_medicationAdministrations'] = [occurrence_medicationAdministration,]
                                    occurrence_medicationAdministration = {}
                                else:
                                    if stepresult.has_key('medicationAdministrations'):
                                        stepresult['medicationAdministrations'].append(medicationAdministration)
                                    else:
                                        stepresult['medicationAdministrations'] = [medicationAdministration,]
                                    medicationAdministration = {}
                        parent_tag.pop(0)
                        continue

                    if elem.tag in ("ActionGroupResult", "ActionStepResult"):
                        #print "End ", elem.tag
                        if parent_tag[0] == "ActionStepResult":
                            #
                            # For every action record stored, use the id attribute of action_obj
                            # and store it in the action_id field of the following tables
                            #
                            action_obj = ActionResults.objects.create(action_type='ActionStepResult',
                                                                state='Start',
                                                                healthactionresult_id=healthactionresult_obj.id,
                                                                name=stepresult.get('name', None),
                                                                name_type=stepresult.get('name_type', None),
                                                                name_value=stepresult.get('name_value', None),
                                                                name_abbrev=stepresult.get('name_abbrev', None))

                            if stepresult.has_key('occurrences'):
                                for an_occurrence in stepresult['occurrences']:
                                    # Convert datetime fields
                                    startTime = an_occurrence.get('startTime', None)
                                    if startTime != None:
                                        startTime = iso8601.parse_date(startTime)
                                    endTime = an_occurrence.get('endTime', None)
                                    if endTime != None:
                                        endTime = iso8601.parse_date(endTime)
                                    occurrence_obj = Occurrences.objects.create(action_id=action_obj.id,
                                                                                startTime=startTime,
                                                                                endTime=endTime,
                                                                                additionalDetails=an_occurrence.get('additionalDetails', None))

                                    # TODO: Add code responsible for creating the measurements, devicePlans and medicationAdministrations
                                    #       records which relate to this the Occurrence record created above
                                    if stepresult.has_key('occurrence_stopCondition'):
                                        for a_stopCondition in stepresult['occurrence_stopCondition']:
                                            StopConditionResults.objects.create(action_id=action_obj.id,
                                                                                occurrence_id=occurrence_obj.id,
                                                                                name=a_stopCondition.get('name', None),
                                                                                name_type=a_stopCondition.get('name_type', None),
                                                                                name_value=a_stopCondition.get('name_value', None),
                                                                                name_abbrev=a_stopCondition.get('name_abbrev', None),
                                                                                value_textvalue=a_stopCondition.get('value_textvalue', None),
                                                                                value_value=a_stopCondition.get('value_value', None),
                                                                                value_unit=a_stopCondition.get('value_unit', None),
                                                                                value_unit_type=a_stopCondition.get('value_unit_type', None),
                                                                                value_unit_value=a_stopCondition.get('value_unit_value', None),
                                                                                value_unit_abbrev=a_stopCondition.get('value_unit_abbrev', None))

                                    if stepresult.has_key('occurrence_measurements'):
                                        for a_measurement in stepresult['occurrence_measurements']:
                                            Measurements.objects.create(action_id=action_obj.id,
                                                                        occurrence_id=occurrence_obj.id,
                                                                        name=a_measurement.get('name', None),
                                                                        name_type=a_measurement.get('name_type', None),
                                                                        name_value=a_measurement.get('name_value', None),
                                                                        name_abbrev=a_measurement.get('name_abbrev', None),
                                                                        type=a_measurement.get('type', None),
                                                                        type_type=a_measurement.get('type_type', None),
                                                                        type_value=a_measurement.get('type_value', None),
                                                                        type_abbrev=a_measurement.get('type_abbrev', None),
                                                                        value_textvalue=an_occurrence.get('value_textvalue', None),
                                                                        value_value=a_measurement.get('value_value', None),
                                                                        value_unit=a_measurement.get('value_unit', None),
                                                                        value_unit_type=a_measurement.get('value_unit_type', None),
                                                                        value_unit_value=a_measurement.get('value_unit_value', None),
                                                                        value_unit_abbrev=a_measurement.get('value_unit_abbrev', None),
                                                                        aggregationFunction=a_measurement.get('aggregationFunction', None),
                                                                        aggregationFunction_type=a_measurement.get('aggregationFunction_type', None),
                                                                        aggregationFunction_value=a_measurement.get('aggregationFunction_value', None),
                                                                        aggregationFunction_abbrev=a_measurement.get('aggregationFunction_abbrev', None))

                                    if stepresult.has_key('occurrence_deviceResults'):
                                        for a_devicePlan in stepresult['occurrence_deviceResults']:
                                            DeviceResults.objects.create(action_id=action_obj.id,
                                                                         occurrence_id=occurrence_obj.id,
                                                                         name=a_devicePlan.get('name', None),
                                                                         name_type=a_devicePlan.get('name_type', None),
                                                                         name_value=a_devicePlan.get('name_value', None),
                                                                         name_abbrev=a_devicePlan.get('name_abbrev', None),
                                                                         type=a_devicePlan.get('type', None),
                                                                         type_type=a_devicePlan.get('type_type', None),
                                                                         type_value=a_devicePlan.get('type_value', None),
                                                                         type_abbrev=a_devicePlan.get('type_abbrev', None),
                                                                         value_textvalue=a_devicePlan.get('value_textvalue', None),
                                                                         value_value=a_devicePlan.get('value_value', None),
                                                                         value_unit=a_devicePlan.get('value_unit', None),
                                                                         value_unit_type=a_devicePlan.get('value_unit_type', None),
                                                                         value_unit_value=a_devicePlan.get('value_unit_value', None),
                                                                         value_unit_abbrev=a_devicePlan.get('value_unit_abbrev', None),
                                                                         site=a_devicePlan.get('site', None),
                                                                         site_type=a_devicePlan.get('site_type', None),
                                                                         site_value=a_devicePlan.get('site_value', None),
                                                                         site_abbrev=a_devicePlan.get('site_abbrev', None))

                                    if stepresult.has_key('occurrence_medicationAdministrations'):
                                        for a_medicationAdministration in stepresult['occurrence_medicationAdministrations']:
                                            MedicationAdministrations.objects.create(action_id=action_obj.id,
                                                                                     occurrence_id=occurrence_obj.id,
                                                                                     name=a_medicationAdministration.get('name', None),
                                                                                     name_type=a_medicationAdministration.get('name_type', None),
                                                                                     name_value=a_medicationAdministration.get('name_value', None),
                                                                                     name_abbrev=a_medicationAdministration.get('name_abbrev', None),
                                                                                     dose=a_medicationAdministration.get('dose', None),
                                                                                     dose_type=a_medicationAdministration.get('dose_type', None),
                                                                                     dose_value=a_medicationAdministration.get('dose_value', None),
                                                                                     dose_abbrev=a_medicationAdministration.get('dose_abbrev', None),
                                                                                     route_textvalue=a_medicationAdministration.get('route_textvalue', None),
                                                                                     route_value=a_medicationAdministration.get('route_value', None),
                                                                                     route_unit=a_medicationAdministration.get('route_unit', None),
                                                                                     route_unit_type=a_medicationAdministration.get('route_unit_type', None),
                                                                                     route_unit_value=a_medicationAdministration.get('route_unit_value', None),
                                                                                     route_unit_abbrev=a_medicationAdministration.get('route_unit_abbrev', None))


                            if stepresult.has_key('measurements'):
                                for a_measurement in stepresult['measurements']:
                                    Measurements.objects.create(action_id=action_obj.id,
                                                                occurrence_id=None,
                                                                name=a_measurement.get('name', None),
                                                                name_type=a_measurement.get('name_type', None),
                                                                name_value=a_measurement.get('name_value', None),
                                                                name_abbrev=a_measurement.get('name_abbrev', None),
                                                                type=a_measurement.get('type', None),
                                                                type_type=a_measurement.get('type_type', None),
                                                                type_value=a_measurement.get('type_value', None),
                                                                type_abbrev=a_measurement.get('type_abbrev', None),
                                                                value_textvalue=an_occurrence.get('value_textvalue', None),
                                                                value_value=a_measurement.get('value_value', None),
                                                                value_unit=a_measurement.get('value_unit', None),
                                                                value_unit_type=a_measurement.get('value_unit_type', None),
                                                                value_unit_value=a_measurement.get('value_unit_value', None),
                                                                value_unit_abbrev=a_measurement.get('value_unit_abbrev', None),
                                                                aggregationFunction=a_measurement.get('aggregationFunction', None),
                                                                aggregationFunction_type=a_measurement.get('aggregationFunction_type', None),
                                                                aggregationFunction_value=a_measurement.get('aggregationFunction_value', None),
                                                                aggregationFunction_abbrev=a_measurement.get('aggregationFunction_abbrev', None))

                            if stepresult.has_key('deviceResults'):
                                for a_devicePlan in stepresult['deviceResults']:
                                    DeviceResults.objects.create(action_id=action_obj.id,
                                                                 occurrence_id=None,
                                                                 name=a_devicePlan.get('name', None),
                                                                 name_type=a_devicePlan.get('name_type', None),
                                                                 name_value=a_devicePlan.get('name_value', None),
                                                                 name_abbrev=a_devicePlan.get('name_abbrev', None),
                                                                 type=a_devicePlan.get('type', None),
                                                                 type_type=a_devicePlan.get('type_type', None),
                                                                 type_value=a_devicePlan.get('type_value', None),
                                                                 type_abbrev=a_devicePlan.get('type_abbrev', None),
                                                                 value_textvalue=a_devicePlan.get('value_textvalue', None),
                                                                 value_value=a_devicePlan.get('value_value', None),
                                                                 value_unit=a_devicePlan.get('value_unit', None),
                                                                 value_unit_type=a_devicePlan.get('value_unit_type', None),
                                                                 value_unit_value=a_devicePlan.get('value_unit_value', None),
                                                                 value_unit_abbrev=a_devicePlan.get('value_unit_abbrev', None),
                                                                 site=a_devicePlan.get('site', None),
                                                                 site_type=a_devicePlan.get('site_type', None),
                                                                 site_value=a_devicePlan.get('site_value', None),
                                                                 site_abbrev=a_devicePlan.get('site_abbrev', None))

                            if stepresult.has_key('medicationAdministrations'):
                                for a_medicationAdministration in stepresult['medicationAdministrations']:
                                    MedicationAdministrations.objects.create(action_id=action_obj.id,
                                                                             occurrence_id=None,
                                                                             name=a_medicationAdministration.get('name', None),
                                                                             name_type=a_medicationAdministration.get('name_type', None),
                                                                             name_value=a_medicationAdministration.get('name_value', None),
                                                                             name_abbrev=a_medicationAdministration.get('name_abbrev', None),
                                                                             dose=a_medicationAdministration.get('dose', None),
                                                                             dose_type=a_medicationAdministration.get('dose_type', None),
                                                                             dose_value=a_medicationAdministration.get('dose_value', None),
                                                                             dose_abbrev=a_medicationAdministration.get('dose_abbrev', None),
                                                                             route_textvalue=a_medicationAdministration.get('route_textvalue', None),
                                                                             route_value=a_medicationAdministration.get('route_value', None),
                                                                             route_unit=a_medicationAdministration.get('route_unit', None),
                                                                             route_unit_type=a_medicationAdministration.get('route_unit_type', None),
                                                                             route_unit_value=a_medicationAdministration.get('route_unit_value', None),
                                                                             route_unit_abbrev=a_medicationAdministration.get('route_unit_abbrev', None))

                            #
                            # Prepare the following lists for the next ActionStepResult tag
                            #
                            stepresult['measurements'] = []
                            stepresult['deviceResults'] = []
                            stepresult['medicationAdministrations'] = []
                            stepresult['occurrences'] = []
                            stepresult['occurrence_stopCondition'] = []
                            stepresult['occurrence_measurements'] = []
                            stepresult['occurrence_deviceResults'] = []
                            stepresult['occurrence_medicationAdministrations'] = []

                        ActionResults.objects.create(action_type=elem.tag,
                                                     state='end',
                                                     healthactionresult_id=healthactionresult_obj.id)
                        parent_tag.pop(0)
                        continue
            
            return healthactionresult_obj
        except Exception, e:
              raise ValueError("problem processing healthactionresult report " + str(e))
