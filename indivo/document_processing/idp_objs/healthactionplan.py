from indivo.lib import iso8601
from indivo.models import HealthActionPlan
from indivo.models import Actions
from indivo.models import StopConditions
from indivo.models import Targets
from indivo.models import MeasurementPlans
from indivo.models import DevicePlans
from indivo.models import MedicationPlans
from lxml import etree
from StringIO import StringIO
import pprint

class IDP_HealthActionPlan:

    def process(self, root_node_name, xmldom, original_xml):
        """
        moving this to etree
        """
        retval_facts = []

        hap = etree.XML(original_xml)
        actions_element = hap.find('{http://indivo.org/vocab/xml/documents/healthActionPlan#}actions')
        # force the actions_element subtree to contain newlines after each element
        xml_str = etree.tostring(actions_element, pretty_print=True, method="xml")
        actions_element = etree.XML(xml_str)

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
                #new_fact['actions_xml'] = new_fact['actions_xml'].replace('<action xsi:type="ActionGroup">', '<action type="ActionGroup">')
                #new_fact['actions_xml'] = new_fact['actions_xml'].replace('<action xsi:type="ActionStep">', '<action type="ActionStep">')
                retval_facts.append(new_fact)

        if retval_facts:
            return retval_facts
        return False

    def post_data(self, name=None,
                        name_type=None,
                        name_value=None,
                        name_abbrev=None,
                        planType=None,
                        plannedBy=None,
                        datePlanned=None,
                        dateExpires=None,
                        indication=None,
                        instructions=None,
                        system=None,
                        system_type=None,
                        system_value=None,
                        system_abbrev=None,
                        actions=None,
                        actions_xml=None):
        try:
            #
            # The first thing to do is to save just the HealthActionPlan record
            #
            if datePlanned: datePlanned = iso8601.parse_date(datePlanned)
            if dateExpires: dateExpires = iso8601.parse_date(dateExpires)
 
            healthactionplan_obj = HealthActionPlan.objects.create(name=name,
                                                                   name_type=name_type,
                                                                   name_value=name_value,
                                                                   name_abbrev=name_abbrev,
                                                                   planType=planType,
                                                                   plannedBy=plannedBy,
                                                                   datePlanned=datePlanned,
                                                                   dateExpires=dateExpires,
                                                                   indication=indication,
                                                                   instructions=instructions,
                                                                   system=system,
                                                                   system_type=system_type,
                                                                   system_value=system_value,
                                                                   system_abbrev=system_abbrev,
                                                                   actions=actions_xml)

            #
            # With the healthactionplan_obj, take the value of the "id" field
            # and store it in each action record's healthactionplan_id field
            #


            #import pdb; pdb.set_trace()
            #root = etree.XML(actions_xml)
            #print etree.tostring(root, pretty_print=True, method="xml")
            context = etree.iterparse(StringIO(actions), events=("start", "end"))

            stopCondition = {}
            target = {}
            measurementPlan = {}
            devicePlan = {}
            medicationPlan = {}
            groupplan = {}
            stepplan = {}
            action_type = ''

            parent_tag = []

            action_obj = None

            #import pdb; pdb.set_trace()
            for action, elem in context:
                #print("%s: %s :%s" % (action, elem.tag, elem.text))
                if elem.tag in ("actions", "stopConditions", "targets", "measurementPlans", "devicePlans", "medicationPlans"):
                    # I don't care about these tags
                    continue

                if action == "start":

                    #if elem.tag == "ActionStep":
                    if elem.tag in ("ActionGroup", "ActionStep"):
                        #print "Start ", elem.tag
                        if action_type == "ActionGroup":
                            #print "Start ", elem.tag

                            #
                            # For every action record stored, use the id attribute of action_obj
                            # and store it in the action_id field of the following tables
                            #
                            action_obj = Actions.objects.create(action_type='ActionGroup',
                                                   state='Start',
                                                   healthactionplan_id=healthactionplan_obj.id,
                                                   position=groupplan.get('position', None),
                                                   position_type=groupplan.get('position_type', None),
                                                   position_value=groupplan.get('position_value', None),
                                                   position_abbrev=groupplan.get('position_abbrev', None),
                                                   repeatCount=groupplan.get('repeatCount', 0))

                            if groupplan.has_key('stopConditions'):
                                for a_stopCondition in groupplan['stopConditions']:
                                    StopConditions.objects.create(action_id=action_obj.id,
                                                                  name=a_stopCondition.get('name', None),
                                                                  name_type=a_stopCondition.get('name_type', None),
                                                                  name_value=a_stopCondition.get('name_value', None),
                                                                  name_abbrev=a_stopCondition.get('name_abbrev', None),
                                                                  value_textvalue=a_stopCondition.get('value_textvalue', None),
                                                                  value_value=a_stopCondition.get('value_value', None),
                                                                  value_unit=a_stopCondition.get('value_unit', None),
                                                                  value_unit_type=a_stopCondition.get('value_unit_type', None),
                                                                  value_unit_value=a_stopCondition.get('value_unit_value', None),
                                                                  value_unit_abbrev=a_stopCondition.get('value_unit_abbrev', None),
                                                                  operator=a_stopCondition.get('operator', None),
                                                                  operator_type=a_stopCondition.get('operator_type', None),
                                                                  operator_value=a_stopCondition.get('operator_value', None),
                                                                  operator_abbrev=a_stopCondition.get('operator_abbrev', None),
                                                                  detail=a_stopCondition.get('detail', None),
                                                                  detail_type=a_stopCondition.get('detail_type', None),
                                                                  detail_value=a_stopCondition.get('detail_value', None),
                                                                  detail_abbrev=a_stopCondition.get('detail_abbrev', None))

                            if groupplan.has_key('targets'):
                                for a_target in groupplan['targets']:
                                    Targets.objects.create(action_id=action_obj.id,
                                                           name=a_target.get('name', None),
                                                           name_type=a_target.get('name_type', None),
                                                           name_value=a_target.get('name_value', None),
                                                           name_abbrev=a_target.get('name_abbrev', None),
                                                           minimumValue_textvalue=a_target.get('minimumValue_textvalue', None),
                                                           minimumValue_value=a_target.get('minimumValue_value', None),
                                                           minimumValue_unit=a_target.get('minimumValue_unit', None),
                                                           minimumValue_unit_type=a_target.get('minimumValue_unit_type', None),
                                                           minimumValue_unit_value=a_target.get('minimumValue_unit_value', None),
                                                           minimumValue_unit_abbrev=a_target.get('minimumValue_unit_abbrev', None),
                                                           maximumValue_textvalue=a_target.get('maximumValue_textvalue', None),
                                                           maximumValue_value=a_target.get('maximumValue_value', None),
                                                           maximumValue_unit=a_target.get('maximumValue_unit', None),
                                                           maximumValue_unit_type=a_target.get('maximumValue_unit_type', None),
                                                           maximumValue_unit_value=a_target.get('maximumValue_unit_value', None),
                                                           maximumValue_unit_abbrev=a_target.get('maximumValue_unit_abbrev', None),
                                                           securityLevel=a_target.get('securityLevel', None),
                                                           securityLevel_type=a_target.get('securityLevel_type', None),
                                                           securityLevel_value=a_target.get('securityLevel_value', None),
                                                           securityLevel_abbrev=a_target.get('securityLevel_abbrev', None))

                            if groupplan.has_key('measurementPlans'):
                                for a_measurementPlan in groupplan['measurementPlans']:
                                    MeasurementPlans.objects.create(action_id=action_obj.id,
                                                                    name=a_measurementPlan.get('name', None),
                                                                    name_type=a_measurementPlan.get('name_type', None),
                                                                    name_value=a_measurementPlan.get('name_value', None),
                                                                    name_abbrev=a_measurementPlan.get('name_abbrev', None),
                                                                    type=a_measurementPlan.get('type', None),
                                                                    type_type=a_measurementPlan.get('type_type', None),
                                                                    type_value=a_measurementPlan.get('type_value', None),
                                                                    type_abbrev=a_measurementPlan.get('type_abbrev', None),
                                                                    aggregationFunction=a_measurementPlan.get('aggregationFunction', None),
                                                                    aggregationFunction_type=a_measurementPlan.get('aggregationFunction_type', None),
                                                                    aggregationFunction_value=a_measurementPlan.get('aggregationFunction_value', None),
                                                                    aggregationFunction_abbrev=a_measurementPlan.get('aggregationFunction_abbrev', None))

                            if groupplan.has_key('devicePlans'):
                                for a_devicePlan in groupplan['devicePlans']:
                                    DevicePlans.objects.create(action_id=action_obj.id,
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
                                                               site_abbrev=a_devicePlan.get('site_abbrev', None),
                                                               instructions=a_devicePlan.get('instructions', None))

                            if groupplan.has_key('medicationPlans'):
                                for a_medicationPlan in groupplan['medicationPlans']:
                                    MedicationPlans.objects.create(action_id=action_obj.id,
                                                                   name=a_medicationPlan.get('name', None),
                                                                   name_type=a_medicationPlan.get('name_type', None),
                                                                   name_value=a_medicationPlan.get('name_value', None),
                                                                   name_abbrev=a_medicationPlan.get('name_abbrev', None),
                                                                   indication=a_medicationPlan.get('instructions', None),
                                                                   dose_textvalue=a_medicationPlan.get('dose_textvalue', None),
                                                                   dose_value=a_medicationPlan.get('dose_value', None),
                                                                   dose_unit=a_medicationPlan.get('dose_unit', None),
                                                                   dose_unit_type=a_medicationPlan.get('dose_unit_type', None),
                                                                   dose_unit_value=a_medicationPlan.get('dose_unit_value', None),
                                                                   dose_unit_abbrev=a_medicationPlan.get('dose_unit_abbrev', None),
                                                                   route=a_medicationPlan.get('route', None),
                                                                   route_type=a_medicationPlan.get('route_type', None),
                                                                   route_value=a_medicationPlan.get('route_value', None),
                                                                   route_abbrev=a_medicationPlan.get('route_abbrev', None))

                            #
                            # Prepare the following lists for the next ActionGroup tag
                            #
                            groupplan['stopConditions'] = []
                            groupplan['targets'] = []
                            groupplan['measurementPlans'] = []
                            groupplan['devicePlans'] = []
                            groupplan['medicationPlans'] = []
                        
                        if elem.tag == "ActionGroup":
                            #
                            # Make preparations for another ActionGroup element
                            #
                            action_type = 'ActionGroup'
                            groupplan = {"action_type" : "ActionGroup"}
                            groupplan['state'] = 'start'
                            groupplan['repeatCount'] = None
                            parent_tag.insert(0, elem.tag)

                        if elem.tag == 'ActionStep':
                            #
                            # Make preparations for another ActionGroup element
                            #
                            action_type = 'ActionStep'
                            stepplan = {"action_type" : "ActionStep"}
                            stepplan['state'] = 'start'
                            stepplan['name'] = None
                            stepplan['name_type'] = None
                            stepplan['name_value'] = None
                            stepplan['name_abbrev'] = None
                            stepplan['type'] = None
                            stepplan['type_type'] = None
                            stepplan['type_value'] = None
                            stepplan['type_abbrev'] = None
                            stepplan['additionalDetails'] = None
                            stepplan['instructions'] = None
                            parent_tag.insert(0, elem.tag)
                        
                        continue

                    if elem.tag in ("stopCondition", "target", "measurementPlan", "devicePlan", "medicationPlan"):
                        parent_tag.insert(0, elem.tag)
                        continue

                    #if len(parent_tag) == 0: continue

                    if parent_tag[0] in ("stopCondition", "target", "measurementPlan", "devicePlan", "medicationPlan"):
                        #print parent_tag[0], ' : ', elem.tag, ' : ', elem.text
                        if parent_tag[0] == "stopCondition":
                            stopCondition[elem.tag] = elem.text
                            continue
                        if parent_tag[0] == "target":
                            target[elem.tag] = elem.text
                            continue
                        if parent_tag[0] == "measurementPlan":
                            measurementPlan[elem.tag] = elem.text
                            continue
                        if parent_tag[0] == "devicePlan":
                            devicePlan[elem.tag] = elem.text
                            continue
                        if parent_tag[0] == "medicationPlan":
                            medicationPlan[elem.tag] = elem.text
                            continue

                    if parent_tag[0] == 'ActionGroup':
                        groupplan[elem.tag] = elem.text
                    if parent_tag[0] == 'ActionStep':
                        stepplan[elem.tag] = elem.text


                if action == "end":
                    
                    if elem.tag in ("stopCondition", "target", "measurementPlan", "devicePlan", "medicationPlan"):
                        #print "***GROUP*****"
                        #pprint.pprint(groupplan)
                        #print "------STEP---"
                        #pprint.pprint(stepplan)
                        #print parent_tag[0], ' : ', elem.tag, ' : ', elem.text
                        if elem.tag == "stopCondition" and len(stopCondition) > 0:
                            if action_type == 'ActionGroup':
                                if groupplan.has_key('stopConditions'):
                                    groupplan['stopConditions'].append(stopCondition)
                                else:
                                    groupplan['stopConditions'] = [stopCondition,]
                            else:
                                if stepplan.has_key('stopConditions'):
                                    stepplan['stopConditions'].append(stopCondition)
                                else:
                                    stepplan['stopConditions'] = [stopCondition,]
                            stopCondition = {}
                        if elem.tag == "target" and len(target) > 0:
                            if action_type == 'ActionGroup':
                                if groupplan.has_key('targets'):
                                    groupplan['targets'].append(target)
                                else:
                                    groupplan['targets'] = [target,]
                            else:
                                if stepplan.has_key('targets'):
                                    stepplan['targets'].append(target)
                                else:
                                    stepplan['targets'] = [target,]
                            target = {}
                        if elem.tag == "measurementPlan" and len(measurementPlan) > 0:
                            if action_type == 'ActionGroup':
                                if groupplan.has_key('measurementPlans'):
                                    groupplan['measurementPlans'].append(measurementPlan)
                                else:
                                    groupplan['measurementPlans'] = [measurementPlan,]
                            else:
                                if stepplan.has_key('measurementPlans'):
                                    stepplan['measurementPlans'].append(measurementPlan)
                                else:
                                    stepplan['measurementPlans'] = [measurementPlan,]
                            measurementPlan = {}
                        if elem.tag == "devicePlan" and len(devicePlan) > 0:
                            if action_type == 'ActionGroup':
                                if groupplan.has_key('devicePlans'):
                                    groupplan['devicePlans'].append(devicePlan)
                                else:
                                    groupplan['devicePlans'] = [devicePlan,]
                            else:
                                if stepplan.has_key('devicePlan'):
                                    stepplan['devicePlans'].append(devicePlan)
                                else:
                                    stepplan['devicePlans'] = [devicePlan,]
                            devicePlan = {}
                        if elem.tag == "medicationPlan" and len(medicationPlan) > 0:
                            if action_type == 'ActionGroup':
                                if groupplan.has_key('medicationPlans'):
                                    groupplan['medicationPlans'].append(medicationPlan)
                                else:
                                    groupplan['medicationPlans'] = [medicationPlan,]
                            else:
                                if stepplan.has_key('medicationPlans'):
                                    stepplan['medicationPlans'].append(medicationPlan)
                                else:
                                    stepplan['medicationPlans'] = [medicationPlan,]
                            medicationPlan = {}
                        parent_tag.pop(0)
                        continue

                    if elem.tag in ("ActionGroup", "ActionStep"):
                        #print "End ", elem.tag
                        if parent_tag[0] == "ActionStep":
                            #
                            # For every action record stored, use the id attribute of action_obj
                            # and store it in the action_id field of the following tables
                            #
                            action_obj = Actions.objects.create(action_type=stepplan['action_type'],
                                                                state=stepplan['state'],
                                                                healthactionplan_id=healthactionplan_obj.id,
                                                                position=stepplan.get('position', None),
                                                                position_type=stepplan.get('position_type', None),
                                                                position_value=stepplan.get('position_value', None),
                                                                position_abbrev=stepplan.get('position_abbrev', None),
                                                                name=stepplan.get('name', None),
                                                                name_type=stepplan.get('name_type', None),
                                                                name_value=stepplan.get('name_value', None),
                                                                name_abbrev=stepplan.get('name_abbrev', None),
                                                                type=stepplan.get('type', None),
                                                                type_type=stepplan.get('type_type', None),
                                                                type_value=stepplan.get('type_value', None),
                                                                type_abbrev=stepplan.get('type_abbrev', None),
                                                                additionalDetails=stepplan.get('additionalDetails', None),
                                                                instructions=stepplan.get('instructions', None))

                            if stepplan.has_key('stopConditions'):
                                for a_stopCondition in stepplan['stopConditions']:
                                    StopConditions.objects.create(action_id=action_obj.id,
                                                                  name=a_stopCondition.get('name', None),
                                                                  name_type=a_stopCondition.get('name_type', None),
                                                                  name_value=a_stopCondition.get('name_value', None),
                                                                  name_abbrev=a_stopCondition.get('name_abbrev', None),
                                                                  value_textvalue=a_stopCondition.get('value_textvalue', None),
                                                                  value_value=a_stopCondition.get('value_value', None),
                                                                  value_unit=a_stopCondition.get('value_unit', None),
                                                                  value_unit_type=a_stopCondition.get('value_unit_type', None),
                                                                  value_unit_value=a_stopCondition.get('value_unit_value', None),
                                                                  value_unit_abbrev=a_stopCondition.get('value_unit_abbrev', None),
                                                                  operator=a_stopCondition.get('operator', None),
                                                                  operator_type=a_stopCondition.get('operator_type', None),
                                                                  operator_value=a_stopCondition.get('operator_value', None),
                                                                  operator_abbrev=a_stopCondition.get('operator_abbrev', None),
                                                                  detail=a_stopCondition.get('detail', None),
                                                                  detail_type=a_stopCondition.get('detail_type', None),
                                                                  detail_value=a_stopCondition.get('detail_value', None),
                                                                  detail_abbrev=a_stopCondition.get('detail_abbrev', None))

                            if stepplan.has_key('targets'):
                                for a_target in stepplan['targets']:
                                    Targets.objects.create(action_id=action_obj.id,
                                                           name=a_target.get('name', None),
                                                           name_type=a_target.get('name_type', None),
                                                           name_value=a_target.get('name_value', None),
                                                           name_abbrev=a_target.get('name_abbrev', None),
                                                           minimumValue_textvalue=a_target.get('minimumValue_textvalue', None),
                                                           minimumValue_value=a_target.get('minimumValue_value', None),
                                                           minimumValue_unit=a_target.get('minimumValue_unit', None),
                                                           minimumValue_unit_type=a_target.get('minimumValue_unit_type', None),
                                                           minimumValue_unit_value=a_target.get('minimumValue_unit_value', None),
                                                           minimumValue_unit_abbrev=a_target.get('minimumValue_unit_abbrev', None),
                                                           maximumValue_textvalue=a_target.get('maximumValue_textvalue', None),
                                                           maximumValue_value=a_target.get('maximumValue_value', None),
                                                           maximumValue_unit=a_target.get('maximumValue_unit', None),
                                                           maximumValue_unit_type=a_target.get('maximumValue_unit_type', None),
                                                           maximumValue_unit_value=a_target.get('maximumValue_unit_value', None),
                                                           maximumValue_unit_abbrev=a_target.get('maximumValue_unit_abbrev', None),
                                                           securityLevel=a_target.get('securityLevel', None),
                                                           securityLevel_type=a_target.get('securityLevel_type', None),
                                                           securityLevel_value=a_target.get('securityLevel_value', None),
                                                           securityLevel_abbrev=a_target.get('securityLevel_abbrev', None))

                            if stepplan.has_key('measurementPlans'):
                                for a_measurementPlan in stepplan['measurementPlans']:
                                    MeasurementPlans.objects.create(action_id=action_obj.id,
                                                                    name=a_measurementPlan.get('name', None),
                                                                    name_type=a_measurementPlan.get('name_type', None),
                                                                    name_value=a_measurementPlan.get('name_value', None),
                                                                    name_abbrev=a_measurementPlan.get('name_abbrev', None),
                                                                    type=a_measurementPlan.get('type', None),
                                                                    type_type=a_measurementPlan.get('type_type', None),
                                                                    type_value=a_measurementPlan.get('type_value', None),
                                                                    type_abbrev=a_measurementPlan.get('type_abbrev', None),
                                                                    aggregationFunction=a_measurementPlan.get('aggregationFunction', None),
                                                                    aggregationFunction_type=a_measurementPlan.get('aggregationFunction_type', None),
                                                                    aggregationFunction_value=a_measurementPlan.get('aggregationFunction_value', None),
                                                                    aggregationFunction_abbrev=a_measurementPlan.get('aggregationFunction_abbrev', None))

                            if stepplan.has_key('devicePlans'):
                                for a_devicePlan in stepplan['devicePlans']:
                                    DevicePlans.objects.create(action_id=action_obj.id,
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
                                                               site_abbrev=a_devicePlan.get('site_abbrev', None),
                                                               instructions=a_devicePlan.get('instructions', None))

                            if stepplan.has_key('medicationPlans'):
                                for a_medicationPlan in stepplan['medicationPlans']:
                                    MedicationPlans.objects.create(action_id=action_obj.id,
                                                                   name=a_medicationPlan.get('name', None),
                                                                   name_type=a_medicationPlan.get('name_type', None),
                                                                   name_value=a_medicationPlan.get('name_value', None),
                                                                   name_abbrev=a_medicationPlan.get('name_abbrev', None),
                                                                   indication=a_medicationPlan.get('instructions', None),
                                                                   dose_textvalue=a_medicationPlan.get('dose_textvalue', None),
                                                                   dose_value=a_medicationPlan.get('dose_value', None),
                                                                   dose_unit=a_medicationPlan.get('dose_unit', None),
                                                                   dose_unit_type=a_medicationPlan.get('dose_unit_type', None),
                                                                   dose_unit_value=a_medicationPlan.get('dose_unit_value', None),
                                                                   dose_unit_abbrev=a_medicationPlan.get('dose_unit_abbrev', None),
                                                                   route=a_medicationPlan.get('route', None),
                                                                   route_type=a_medicationPlan.get('route_type', None),
                                                                   route_value=a_medicationPlan.get('route_value', None),
                                                                   route_abbrev=a_medicationPlan.get('route_abbrev', None))

                            #
                            # Prepare the following lists for the next ActionStep tag
                            #
                            stepplan['stopConditions'] = []
                            stepplan['targets'] = []
                            stepplan['measurementPlans'] = []
                            stepplan['devicePlans'] = []
                            stepplan['medicationPlans'] = []

                        Actions.objects.create(action_type=elem.tag,
                                               state='end',
                                               healthactionplan_id=healthactionplan_obj.id)
                        parent_tag.pop(0)
                        continue
            
            return healthactionplan_obj
        except Exception, e:
              raise ValueError("problem processing healthactionplan report " + str(e))
