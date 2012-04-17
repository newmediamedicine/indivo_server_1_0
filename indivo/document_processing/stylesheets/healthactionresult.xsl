<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> 
    <xsl:output method = "xml" indent = "yes" />  
    <xsl:template match="indivodoc:HealthActionResult">
    <facts>
        <fact>
            <name><xsl:value-of select='indivodoc:name/text()' /></name>
            <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
            <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
            <planType><xsl:value-of select='indivodoc:planType/text()' /></planType>
            <reportedBy><xsl:value-of select='indivodoc:reportedBy/text()' /></reportedBy>
            <dateReported><xsl:value-of select='indivodoc:dateReported/text()' /></dateReported>
            <actions_xml><xsl:value-of select='indivodoc:actions_xml/text()' /></actions_xml>
            <actions><xsl:apply-templates select="indivodoc:actions" /></actions>
        </fact>
    </facts>
    </xsl:template>

    <xsl:template match="indivodoc:route">
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

    <xsl:template match="indivodoc:value">
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

    <xsl:template match="indivodoc:actions">
        <xsl:apply-templates select="indivodoc:action" />
    </xsl:template>

    <xsl:template match="indivodoc:action">
        <xsl:choose>
            <xsl:when test="@xsi:type='ActionGroupResult'">
                <ActionGroupResult>
                    <measurements><xsl:apply-templates select="indivodoc:measurements" /></measurements>
                    <deviceResults><xsl:apply-templates select="indivodoc:deviceResults" /></deviceResults>
                    <medicationAdministrations><xsl:apply-templates select="indivodoc:medicationAdministrations" /></medicationAdministrations>
                    <actions><xsl:apply-templates select="indivodoc:actions" /></actions>
                </ActionGroupResult>
            </xsl:when>
            <xsl:otherwise>
                <ActionStepResult>
                    <measurements><xsl:apply-templates select="indivodoc:measurements" /></measurements>
                    <deviceResults><xsl:apply-templates select="indivodoc:deviceResults" /></deviceResults>
                    <medicationAdministrations><xsl:apply-templates select="indivodoc:medicationAdministrations" /></medicationAdministrations>
                    <name><xsl:value-of select='indivodoc:name/text()' /></name>
                    <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
                    <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
                    <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
                    <occurrences><xsl:apply-templates select="indivodoc:occurrences" /></occurrences>
                </ActionStepResult>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="indivodoc:occurrences">
        <xsl:apply-templates select="indivodoc:occurrence" />
    </xsl:template>

    <xsl:template match="indivodoc:occurrence">
        <occurrence>
            <xsl:if test="indivodoc:startTime">
            <startTime><xsl:value-of select='indivodoc:startTime/text()' /></startTime>
            </xsl:if>
            <xsl:if test="indivodoc:endTime">
            <endTime><xsl:value-of select='indivodoc:endTime/text()' /></endTime>
            </xsl:if>
            <xsl:if test="indivodoc:additionalDetails">
            <additionalDetails><xsl:value-of select='indivodoc:additionalDetails/text()' /></additionalDetails>
            </xsl:if>
            <stopConditions><xsl:apply-templates select="indivodoc:stopConditions" /></stopConditions>
            <measurements><xsl:apply-templates select="indivodoc:measurements" /></measurements>
            <deviceResults><xsl:apply-templates select="indivodoc:deviceResults" /></deviceResults>
            <medicationAdministrations><xsl:apply-templates select="indivodoc:medicationAdministrations" /></medicationAdministrations>
        </occurrence>
    </xsl:template>

    <xsl:template match="indivodoc:stopConditions">
        <xsl:apply-templates select="indivodoc:stopCondition" />
    </xsl:template>

    <xsl:template match="indivodoc:stopCondition">
        <stopCondition>
            <name><xsl:value-of select='indivodoc:name/text()' /></name>
            <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
            <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
            <xsl:apply-templates select="indivodoc:value" />
       </stopCondition>
    </xsl:template>

    <xsl:template match="indivodoc:measurements">
        <xsl:apply-templates select="indivodoc:measurement" />
    </xsl:template>

    <xsl:template match="indivodoc:measurement">
        <measurement>
            <name><xsl:value-of select='indivodoc:name/text()' /></name>
            <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
            <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
            <type><xsl:value-of select='indivodoc:type/text()' /></type>
            <type_type><xsl:value-of select='indivodoc:type/@type' /></type_type>
            <type_value><xsl:value-of select='indivodoc:type/@value' /></type_value>
            <type_abbrev><xsl:value-of select='indivodoc:type/@abbrev' /></type_abbrev>
            <xsl:apply-templates select="indivodoc:value" />
            <aggregationFunction><xsl:value-of select='indivodoc:aggregationFunction/text()' /></aggregationFunction>
            <aggregationFunction_type><xsl:value-of select='indivodoc:aggregationFunction/@type' /></aggregationFunction_type>
            <aggregationFunction_value><xsl:value-of select='indivodoc:aggregationFunction/@value' /></aggregationFunction_value>
            <aggregationFunction_abbrev><xsl:value-of select='indivodoc:aggregationFunction/@abbrev' /></aggregationFunction_abbrev>
        </measurement>
    </xsl:template>

    <xsl:template match="indivodoc:deviceResults">
        <xsl:apply-templates select="indivodoc:deviceResult" />
    </xsl:template>

    <xsl:template match="indivodoc:deviceResult">
        <deviceResult>
            <name><xsl:value-of select='indivodoc:name/text()' /></name>
            <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
            <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
            <type><xsl:value-of select='indivodoc:type/text()' /></type>
            <type_type><xsl:value-of select='indivodoc:type/@type' /></type_type>
            <type_value><xsl:value-of select='indivodoc:type/@value' /></type_value>
            <type_abbrev><xsl:value-of select='indivodoc:type/@abbrev' /></type_abbrev>
            <xsl:apply-templates select="indivodoc:value" />
            <site><xsl:value-of select='indivodoc:site/text()' /></site>
            <site_type><xsl:value-of select='indivodoc:site/@type' /></site_type>
            <site_value><xsl:value-of select='indivodoc:site/@value' /></site_value>
            <site_abbrev><xsl:value-of select='indivodoc:site/@abbrev' /></site_abbrev>
        </deviceResult>
    </xsl:template>

    <xsl:template match="indivodoc:medicationAdministrations">
        <xsl:apply-templates select="indivodoc:medicationAdministration" />
    </xsl:template>

    <xsl:template match="indivodoc:medicationAdministration">
        <medicationAdministration>
            <name><xsl:value-of select='indivodoc:name/text()' /></name>
            <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
            <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
            <dose><xsl:value-of select='indivodoc:dose/text()' /></dose>
            <dose_type><xsl:value-of select='indivodoc:dose/@type' /></dose_type>
            <dose_value><xsl:value-of select='indivodoc:dose/@value' /></dose_value>
            <dose_abbrev><xsl:value-of select='indivodoc:dose/@abbrev' /></dose_abbrev>
            <xsl:apply-templates select="indivodoc:route" />
        </medicationAdministration>
    </xsl:template>

</xsl:stylesheet>
