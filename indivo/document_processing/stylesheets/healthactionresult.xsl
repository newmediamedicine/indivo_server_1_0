<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#" xmlns:result="http://indivo.org/vocab/xml/documents/healthActionResult#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <xsl:output method = "xml" indent = "yes" />  
    <xsl:template match="result:HealthActionResult">
    <facts>
        <fact>
            <name><xsl:value-of select='result:name/text()' /></name>
            <name_type><xsl:value-of select='result:name/@type' /></name_type>
            <name_value><xsl:value-of select='result:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='result:name/@abbrev' /></name_abbrev>
            <planType><xsl:value-of select='result:planType/text()' /></planType>
            <reportedBy><xsl:value-of select='result:reportedBy/text()' /></reportedBy>
            <dateReported><xsl:value-of select='result:dateReported/text()' /></dateReported>
            <actions_xml><xsl:value-of select='result:actions_xml/text()' /></actions_xml>
            <actions><xsl:apply-templates select="result:actions" /></actions>
        </fact>
    </facts>
    </xsl:template>

    <xsl:template match="result:route">
        <xsl:if test="indivodoc:textValue">
            <route_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></route_textvalue>
        </xsl:if>
        <xsl:if test="indivodoc:value">
            <route_value><xsl:value-of select='indivodoc:value/text()' /></route_value>
        </xsl:if>
        <xsl:if test="indivodoc:unit">
            <route_unit><xsl:value-of select='indivodoc:unit/text()' /></route_unit>
            <route_unit_type><xsl:value-of select='indivodoc:unit/@type' /></route_unit_type>
            <route_unit_value><xsl:value-of select='indivodoc:unit/@value' /></route_unit_value>
            <route_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></route_unit_abbrev>
        </xsl:if>
    </xsl:template>

    <xsl:template match="result:value">
        <xsl:if test="indivodoc:textValue">
            <value_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></value_textvalue>
        </xsl:if>
        <xsl:if test="indivodoc:value">
            <value_value><xsl:value-of select='indivodoc:value/text()' /></value_value>
        </xsl:if>
        <xsl:if test="indivodoc:unit">
            <value_unit><xsl:value-of select='indivodoc:unit/text()' /></value_unit>
            <value_unit_type><xsl:value-of select='indivodoc:unit/@type' /></value_unit_type>
            <value_unit_value><xsl:value-of select='indivodoc:unit/@value' /></value_unit_value>
            <value_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></value_unit_abbrev>
        </xsl:if>
    </xsl:template>

    <xsl:template match="result:actions">
        <xsl:apply-templates select="result:action" />
    </xsl:template>

    <xsl:template match="result:action">
        <xsl:choose>
            <xsl:when test="@xsi:type='ActionGroupResult'">
                <ActionGroupResult>
                    <measurements><xsl:apply-templates select="result:measurements" /></measurements>
                    <deviceResults><xsl:apply-templates select="result:deviceResults" /></deviceResults>
                    <medicationAdministrations><xsl:apply-templates select="result:medicationAdministrations" /></medicationAdministrations>
                    <actions><xsl:apply-templates select="result:actions" /></actions>
                </ActionGroupResult>
            </xsl:when>
            <xsl:otherwise>
                <ActionStepResult>
                    <measurements><xsl:apply-templates select="result:measurements" /></measurements>
                    <deviceResults><xsl:apply-templates select="result:deviceResults" /></deviceResults>
                    <medicationAdministrations><xsl:apply-templates select="result:medicationAdministrations" /></medicationAdministrations>
                    <name><xsl:value-of select='result:name/text()' /></name>
                    <name_type><xsl:value-of select='result:name/@type' /></name_type>
                    <name_value><xsl:value-of select='result:name/@value' /></name_value>
                    <name_abbrev><xsl:value-of select='result:name/@abbrev' /></name_abbrev>
                    <occurrences><xsl:apply-templates select="result:occurrences" /></occurrences>
                </ActionStepResult>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="result:occurrences">
        <xsl:apply-templates select="result:occurrence" />
    </xsl:template>

    <xsl:template match="result:occurrence">
        <occurrence>
            <xsl:if test="result:startTime">
            <startTime><xsl:value-of select='result:startTime/text()' /></startTime>
            </xsl:if>
            <xsl:if test="result:endTime">
            <endTime><xsl:value-of select='result:endTime/text()' /></endTime>
            </xsl:if>
            <xsl:if test="result:additionalDetails">
            <additionalDetails><xsl:value-of select='result:additionalDetails/text()' /></additionalDetails>
            </xsl:if>
            <stopConditions><xsl:apply-templates select="result:stopConditions" /></stopConditions>
            <measurements><xsl:apply-templates select="result:measurements" /></measurements>
            <deviceResults><xsl:apply-templates select="result:deviceResults" /></deviceResults>
            <medicationAdministrations><xsl:apply-templates select="result:medicationAdministrations" /></medicationAdministrations>
        </occurrence>
    </xsl:template>

    <xsl:template match="result:stopConditions">
        <xsl:apply-templates select="result:stopCondition" />
    </xsl:template>

    <xsl:template match="result:stopCondition">
        <stopCondition>
            <name><xsl:value-of select='result:name/text()' /></name>
            <name_type><xsl:value-of select='result:name/@type' /></name_type>
            <name_value><xsl:value-of select='result:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='result:name/@abbrev' /></name_abbrev>
            <xsl:apply-templates select="result:value" />
       </stopCondition>
    </xsl:template>

    <xsl:template match="result:measurements">
        <xsl:apply-templates select="result:measurement" />
    </xsl:template>

    <xsl:template match="result:measurement">
        <measurement>
            <name><xsl:value-of select='result:name/text()' /></name>
            <name_type><xsl:value-of select='result:name/@type' /></name_type>
            <name_value><xsl:value-of select='result:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='result:name/@abbrev' /></name_abbrev>
            <type><xsl:value-of select='result:type/text()' /></type>
            <type_type><xsl:value-of select='result:type/@type' /></type_type>
            <type_value><xsl:value-of select='result:type/@value' /></type_value>
            <type_abbrev><xsl:value-of select='result:type/@abbrev' /></type_abbrev>
            <xsl:apply-templates select="result:value" />
            <aggregationFunction><xsl:value-of select='result:aggregationFunction/text()' /></aggregationFunction>
            <aggregationFunction_type><xsl:value-of select='result:aggregationFunction/@type' /></aggregationFunction_type>
            <aggregationFunction_value><xsl:value-of select='result:aggregationFunction/@value' /></aggregationFunction_value>
            <aggregationFunction_abbrev><xsl:value-of select='result:aggregationFunction/@abbrev' /></aggregationFunction_abbrev>
        </measurement>
    </xsl:template>

    <xsl:template match="result:deviceResults">
        <xsl:apply-templates select="result:deviceResult" />
    </xsl:template>

    <xsl:template match="result:deviceResult">
        <deviceResult>
            <name><xsl:value-of select='result:name/text()' /></name>
            <name_type><xsl:value-of select='result:name/@type' /></name_type>
            <name_value><xsl:value-of select='result:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='result:name/@abbrev' /></name_abbrev>
            <type><xsl:value-of select='result:type/text()' /></type>
            <type_type><xsl:value-of select='result:type/@type' /></type_type>
            <type_value><xsl:value-of select='result:type/@value' /></type_value>
            <type_abbrev><xsl:value-of select='result:type/@abbrev' /></type_abbrev>
            <xsl:apply-templates select="result:value" />
            <site><xsl:value-of select='result:site/text()' /></site>
            <site_type><xsl:value-of select='result:site/@type' /></site_type>
            <site_value><xsl:value-of select='result:site/@value' /></site_value>
            <site_abbrev><xsl:value-of select='result:site/@abbrev' /></site_abbrev>
        </deviceResult>
    </xsl:template>

    <xsl:template match="result:medicationAdministrations">
        <xsl:apply-templates select="result:medicationAdministration" />
    </xsl:template>

    <xsl:template match="result:medicationAdministration">
        <medicationAdministration>
            <name><xsl:value-of select='result:name/text()' /></name>
            <name_type><xsl:value-of select='result:name/@type' /></name_type>
            <name_value><xsl:value-of select='result:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='result:name/@abbrev' /></name_abbrev>
            <dose><xsl:value-of select='result:dose/text()' /></dose>
            <dose_type><xsl:value-of select='result:dose/@type' /></dose_type>
            <dose_value><xsl:value-of select='result:dose/@value' /></dose_value>
            <dose_abbrev><xsl:value-of select='result:dose/@abbrev' /></dose_abbrev>
            <xsl:apply-templates select="result:route" />
        </medicationAdministration>
    </xsl:template>

</xsl:stylesheet>
