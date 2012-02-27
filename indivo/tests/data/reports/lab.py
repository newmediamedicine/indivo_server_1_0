from base import report_content_to_test_docs

_TEST_LABS = [
"""
<Lab xmlns="http://indivo.org/vocab/xml/documents#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> 
  <dateMeasured>2009-07-16T12:00:00Z</dateMeasured>
  <labType>hematology</labType> 
  <laboratory> 
    <name>Quest</name>
    <address>300 Longwood Ave, Boston MA 02215</address>
  </laboratory>
  <labPanel>
    <name type="http://codes.indivo.org/labs/panels#" abbrev="cbc" value="CBC">CBC</name> 
    <labTest xsi:type="SingleResultLabTest"> 
      <dateMeasured>2009-07-16T12:23:00Z</dateMeasured> 
      <name type="http://codes.indivo.org/labs/tests#" abbrev="Hct" value="evf">evf</name>
      <final>true</final>
      <result xsi:type="ResultInRange"> 
        <flag type="http://codes.indivo.org/hl7/abnormal-flags#" abbrev="A" value="abnormal" /> 
        <valueAndUnit> 
          <value>49</value> 
          <unit type="http://codes.indivo.org/units#" abbrev="%" value="percentage" /> 
        </valueAndUnit> 
        <normalRange> 
          <minimum>44</minimum> 
          <maximum>48</maximum> 
          <unit type="http://codes.indivo.org/units#" abbrev="%" value="percentage" /> 
        </normalRange> 
        <nonCriticalRange> 
          <minimum>42</minimum> 
          <maximum>50</maximum> 
          <unit type="http://codes.indivo.org/units#" abbrev="%" value="percentage" /> 
        </nonCriticalRange> 
      </result> 
    </labTest> 
    <labTest xsi:type="SingleResultLabTest"> 
      <dateMeasured>2009-07-16T12:23:00Z</dateMeasured> 
      <name type="http://codes.indivo.org/labs/tests#" abbrev="hiv" value="HIV">HIV</name> 
      <final>true</final> 
      <result xsi:type="ResultInSet"> 
        <value>negative</value> 
        <option normal="false">positive</option> 
        <option normal="true">negative</option> 
        <option normal="true" description="insufficient sample">inconclusive</option> 
      </result> 
    </labTest> 
  </labPanel> 
  <comments>was looking pretty sick</comments> 
</Lab>
""",

"""
<Lab xmlns="http://indivo.org/vocab/xml/documents#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> 
  <dateMeasured>2009-07-16T12:00:00Z</dateMeasured> 
  <labType>microbiology</labType> 
  <laboratory> 
    <name>Quest</name> 
    <address>300 Longwood Ave, Boston MA 02215</address> 
  </laboratory> 
  <labTest xsi:type="MicroWithCultureLabTest"> 
    <dateMeasured>2009-07-16T12:23:00Z</dateMeasured> 
    <name type="http://codes.indivo.org/labs/tests#" abbrev="mic" value="MIC">MIC</name> 
    <final>true</final>
    <source></source>
    <observation isolate="whoknows"> 
      <time>2009-07-16T12:56:00Z</time>
    </observation> 
    <observation isolate="whoknows"> 
      <time>2009-07-16T13:45:00Z</time> 
      <microbialDensity>
        <value>
          <value>100000</value> 
          <unit type="http://codes.indivo.org/units#" abbrev="cfu" value="CFU" />
        </value> 
      </microbialDensity>
      <cultureCondition>aerobic</cultureCondition> 
      <gram>true</gram> 
      <organization>clusters</organization>
    </observation> 
    <result isolate="what?" identity="1"> 
      <organism>E. Coli</organism> 
      <interpretation>stop eating bad beef</interpretation> 
    </result> 
    <result isolate="who?" identity="2"> 
      <organism>Crazy Bugs</organism> 
      <interpretation>stop eating things that look like beef but aren't</interpretation> 
    </result> 
  </labTest> 
</Lab>
""",

"""
<Lab xmlns="http://indivo.org/vocab/xml/documents#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
   <dateMeasured>2010-09-01T00:00:00Z</dateMeasured>
   <labType>1,25-Dihydroxy Vitamin D</labType>
   <labTest xsi:type="SingleResultLabTest">
      <dateMeasured>2010-09-03T00:00:00Z</dateMeasured>
      <name abbrev="1,25-Dihydroxy Vitamin D">1,25-Dihydroxy Vitamin D</name>
      <final>false</final>
      <result xsi:type="ResultInRange">
         <flag type="http://indivo.org/codes/hl7-abnormal-flags#" value="H" abbrev="H">High</flag>
         <valueAndUnit>
            <value>119.0</value>
            <unit type="http://indivo.org/codes/units#" value="pg/mL" abbrev="pg/mL">pg/mL</unit>
         </valueAndUnit>
      </result>
   </labTest>
   <comments>TEST INFORMATION: Vitamin D, 1,25-Dihydroxy   This test is primarily indicated during patient evaluation for hypercalcemia and renal failure. A normal result does not rule out Vitamin D deficiency. The recommended test for diagnosing Vitamin D deficiency is Vitamin D 25-hydroxy (0080379). Test performed at ARUP Laboratories, 500 Chipeta Way, Salt Lake City, Utah, 84108.</comments>
</Lab>
""",

"""
<Lab xmlns="http://indivo.org/vocab/xml/documents#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> 
  <dateMeasured>1998-07-16T12:00:00Z</dateMeasured> 
  <labType>hematology</labType> 
  <laboratory> 
    <name>Quest</name> 
    <address>300 Longwood Ave, Boston MA 02215</address> 
  </laboratory> 
  <labPanel> 
    <name type="http://codes.indivo.org/labs/panels#" abbrev="cbc" value="CBC">CBC</name> 
    <labTest xsi:type="SingleResultLabTest"> 
      <dateMeasured>2009-07-16T12:23:00Z</dateMeasured> 
      <name type="http://codes.indivo.org/labs/tests#" abbrev="Hct" value="evf">evf</name> 
      <final>true</final> 
      <result xsi:type="ResultInRange"> 
        <flag type="http://codes.indivo.org/hl7/abnormal-flags#" abbrev="A" value="abnormal" /> 
        <valueAndUnit> 
          <value>49</value> 
          <unit type="http://codes.indivo.org/units#" abbrev="%" value="percentage" /> 
        </valueAndUnit> 
        <normalRange> 
          <minimum>44</minimum> 
          <maximum>48</maximum> 
          <unit type="http://codes.indivo.org/units#" abbrev="%" value="percentage" /> 
        </normalRange> 
        <nonCriticalRange> 
          <minimum>42</minimum> 
          <maximum>50</maximum> 
          <unit type="http://codes.indivo.org/units#" abbrev="%" value="percentage" /> 
        </nonCriticalRange> 
      </result> 
    </labTest> 
    <labTest xsi:type="SingleResultLabTest"> 
      <dateMeasured>2009-07-16T12:23:00Z</dateMeasured> 
      <name type="http://codes.indivo.org/labs/tests#" abbrev="hiv" value="HIV">HIV</name> 
      <final>true</final> 
      <result xsi:type="ResultInSet"> 
        <value>negative</value> 
        <option normal="false">positive</option> 
        <option normal="true">negative</option> 
        <option normal="true" description="insufficient sample">inconclusive</option> 
      </result> 
    </labTest> 
  </labPanel> 
  <comments>was looking pretty sick</comments> 
</Lab>
""",
]

TEST_LABS = report_content_to_test_docs(_TEST_LABS)
