<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"> 
    <xsl:output method = "xml" indent = "yes" />  
    <xsl:template match="indivodoc:HealthActionPlan">
    <facts>
        <fact>
            <name><xsl:value-of select='indivodoc:name/text()' /></name>
            <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
            <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
            <planType><xsl:value-of select='indivodoc:planType/text()' /></planType>
            <plannedBy><xsl:value-of select='indivodoc:plannedBy/text()' /></plannedBy>
            <datePlanned><xsl:value-of select='indivodoc:datePlanned/text()' /></datePlanned>
            <xsl:if test="indivodoc:dateExpires">
                <dateExpires><xsl:value-of select='indivodoc:dateExpires/text()' /></dateExpires>
            </xsl:if>
            <indication><xsl:value-of select='indivodoc:indication/text()' /></indication>
            <xsl:if test="indivodoc:instructions">
                <instructions><xsl:value-of select='indivodoc:instructions/text()' /></instructions>
            </xsl:if>
            <xsl:if test="indivodoc:system">
                <system><xsl:value-of select='indivodoc:system/text()' /></system>
                <system_type><xsl:value-of select='indivodoc:system/@type' /></system_type>
                <system_value><xsl:value-of select='indivodoc:system/@value' /></system_value>
                <system_abbrev><xsl:value-of select='indivodoc:system/@abbrev' /></system_abbrev>
            </xsl:if>
            <actions_xml><xsl:value-of select='indivodoc:actions_xml/text()' /></actions_xml>
            <actions><xsl:apply-templates select="indivodoc:actions" /></actions>
        </fact>
    </facts>
    </xsl:template>

    <xsl:template match="indivodoc:dose">
        <xsl:if test="indivodoc:textValue">
            <dose_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></dose_textvalue>
        </xsl:if>
        <xsl:if test="indivodoc:value">
            <dose_value><xsl:value-of select='indivodoc:value/text()' /></dose_value>
        </xsl:if>
        <xsl:if test="indivodoc:unit">
            <dose_unit><xsl:value-of select='indivodoc:unit/text()' /></dose_unit>
            <dose_unit_type><xsl:value-of select='indivodoc:unit/@type' /></dose_unit_type>
            <dose_unit_value><xsl:value-of select='indivodoc:unit/@value' /></dose_unit_value>
            <dose_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></dose_unit_abbrev>
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

    <xsl:template match="indivodoc:minimumValue">
        <xsl:if test="indivodoc:textValue">
            <minimumValue_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></minimumValue_textvalue>
        </xsl:if>
        <xsl:if test="indivodoc:value">
            <minimumValue_value><xsl:value-of select='indivodoc:value/text()' /></minimumValue_value>
        </xsl:if>
        <xsl:if test="indivodoc:unit">
            <minimumValue_unit><xsl:value-of select='indivodoc:unit/text()' /></minimumValue_unit>
            <minimumValue_unit_type><xsl:value-of select='indivodoc:unit/@type' /></minimumValue_unit_type>
            <minimumValue_unit_value><xsl:value-of select='indivodoc:unit/@value' /></minimumValue_unit_value>
            <minimumValue_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></minimumValue_unit_abbrev>
        </xsl:if>
    </xsl:template>

    <xsl:template match="indivodoc:maximumValue">
        <xsl:if test="indivodoc:textValue">
            <maximumValue_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></maximumValue_textvalue>
        </xsl:if>
        <xsl:if test="indivodoc:value">
            <maximumValue_value><xsl:value-of select='indivodoc:value/text()' /></maximumValue_value>
        </xsl:if>
        <xsl:if test="indivodoc:unit">
            <maximumValue_unit><xsl:value-of select='indivodoc:unit/text()' /></maximumValue_unit>
            <maximumValue_unit_type><xsl:value-of select='indivodoc:unit/@type' /></maximumValue_unit_type>
            <maximumValue_unit_value><xsl:value-of select='indivodoc:unit/@value' /></maximumValue_unit_value>
            <maximumValue_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></maximumValue_unit_abbrev>
        </xsl:if>
    </xsl:template>

    <xsl:template match="indivodoc:actions">
        <xsl:apply-templates select="indivodoc:action" />
    </xsl:template>

    <xsl:template match="indivodoc:action">
        <xsl:choose>
            <xsl:when test="@xsi:type='ActionGroup'">
                <ActionGroup>
                    <position><xsl:value-of select='indivodoc:position/text()' /></position>
                    <position_type><xsl:value-of select='indivodoc:position/@type' /></position_type>
                    <position_value><xsl:value-of select='indivodoc:position/@value' /></position_value>
                    <position_abbrev><xsl:value-of select='indivodoc:position/@abbrev' /></position_abbrev>
                    <stopConditions><xsl:apply-templates select="indivodoc:stopConditions" /></stopConditions>
                    <targets><xsl:apply-templates select="indivodoc:targets" /></targets>
                    <measurementPlans><xsl:apply-templates select="indivodoc:measurementPlans" /></measurementPlans>
                    <devicePlans><xsl:apply-templates select="indivodoc:devicePlans" /></devicePlans>
                    <medicationPlans><xsl:apply-templates select="indivodoc:medicationPlans" /></medicationPlans>
                    <repeatCount><xsl:value-of select='indivodoc:repeatCount/text()' /></repeatCount>
                    <actions><xsl:apply-templates select="indivodoc:actions" /></actions>
                </ActionGroup>
            </xsl:when>
            <xsl:otherwise>
                <ActionStep>
                    <position><xsl:value-of select='indivodoc:position/text()' /></position>
                    <position_type><xsl:value-of select='indivodoc:position/@type' /></position_type>
                    <position_value><xsl:value-of select='indivodoc:position/@value' /></position_value>
                    <position_abbrev><xsl:value-of select='indivodoc:position/@abbrev' /></position_abbrev>
                    <stopConditions><xsl:apply-templates select="indivodoc:stopConditions" /></stopConditions>
                    <targets><xsl:apply-templates select="indivodoc:targets" /></targets>
                    <measurementPlans><xsl:apply-templates select="indivodoc:measurementPlans" /></measurementPlans>
                    <devicePlans><xsl:apply-templates select="indivodoc:devicePlans" /></devicePlans>
                    <medicationPlans><xsl:apply-templates select="indivodoc:medicationPlans" /></medicationPlans>
                    <name><xsl:value-of select='indivodoc:name/text()' /></name>
                    <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
                    <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
                    <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
                    <type><xsl:value-of select='indivodoc:type/text()' /></type>
                    <type_type><xsl:value-of select='indivodoc:type/@type' /></type_type>
                    <type_value><xsl:value-of select='indivodoc:type/@value' /></type_value>
                    <type_abbrev><xsl:value-of select='indivodoc:type/@abbrev' /></type_abbrev>
                    <additionalDetails><xsl:value-of select='indivodoc:additionalDetails/text()' /></additionalDetails>
                    <instructions><xsl:value-of select='indivodoc:instructions/text()' /></instructions>
                </ActionStep>
            </xsl:otherwise>
        </xsl:choose>
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
            <operator><xsl:value-of select='indivodoc:operator/text()' /></operator>
            <operator_type><xsl:value-of select='indivodoc:operator/@type' /></operator_type>
            <operator_value><xsl:value-of select='indivodoc:operator/@value' /></operator_value>
            <operator_abbrev><xsl:value-of select='indivodoc:operator/@abbrev' /></operator_abbrev>
            <detail><xsl:value-of select='indivodoc:detail/text()' /></detail>
            <detail_type><xsl:value-of select='indivodoc:detail/@type' /></detail_type>
            <detail_value><xsl:value-of select='indivodoc:detail/@value' /></detail_value>
            <detail_abbrev><xsl:value-of select='indivodoc:detail/@abbrev' /></detail_abbrev>
        </stopCondition>
    </xsl:template>

    <xsl:template match="indivodoc:targets">
        <xsl:apply-templates select="indivodoc:target" />
    </xsl:template>

    <xsl:template match="indivodoc:target">
        <target>
            <name><xsl:value-of select='indivodoc:name/text()' /></name>
            <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
            <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
            <xsl:if test="indivodoc:textValue">
                <minimumValue_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></minimumValue_textvalue>
            </xsl:if>
            <xsl:if test="indivodoc:value">
                <minimumValue_value><xsl:value-of select='indivodoc:value/text()' /></minimumValue_value>
            </xsl:if>
            <xsl:if test="indivodoc:unit">
                <minimumValue_unit><xsl:value-of select='indivodoc:unit/text()' /></minimumValue_unit>
                <minimumValue_unit_type><xsl:value-of select='indivodoc:unit/@type' /></minimumValue_unit_type>
                <minimumValue_unit_value><xsl:value-of select='indivodoc:unit/@value' /></minimumValue_unit_value>
                <minimumValue_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></minimumValue_unit_abbrev>
            </xsl:if>
            <xsl:if test="indivodoc:textValue">
                <maximumValue_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></maximumValue_textvalue>
            </xsl:if>
            <xsl:if test="indivodoc:value">
                <maximumValue_value><xsl:value-of select='indivodoc:value/text()' /></maximumValue_value>
            </xsl:if>
            <xsl:if test="indivodoc:unit">
                <maximumValue_unit><xsl:value-of select='indivodoc:unit/text()' /></maximumValue_unit>
                <maximumValue_unit_type><xsl:value-of select='indivodoc:unit/@type' /></maximumValue_unit_type>
                <maximumValue_unit_value><xsl:value-of select='indivodoc:unit/@value' /></maximumValue_unit_value>
                <maximumValue_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></maximumValue_unit_abbrev>
            </xsl:if>
            <severityLevel><xsl:value-of select='indivodoc:severityLevel/text()' /></severityLevel>
            <severityLevel_type><xsl:value-of select='indivodoc:severityLevel/@type' /></severityLevel_type>
            <severityLevel_value><xsl:value-of select='indivodoc:severityLevel/@value' /></severityLevel_value>
            <severityLevel_abbrev><xsl:value-of select='indivodoc:severityLevel/@abbrev' /></severityLevel_abbrev>
        </target>
    </xsl:template>

    <xsl:template match="indivodoc:measurementPlans">
        <xsl:apply-templates select="indivodoc:measurementPlan" />
    </xsl:template>

    <xsl:template match="indivodoc:measurementPlan">
        <measurementPlan>
            <name><xsl:value-of select='indivodoc:name/text()' /></name>
            <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
            <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
            <type><xsl:value-of select='indivodoc:type/text()' /></type>
            <type_type><xsl:value-of select='indivodoc:type/@type' /></type_type>
            <type_value><xsl:value-of select='indivodoc:type/@value' /></type_value>
            <type_abbrev><xsl:value-of select='indivodoc:type/@abbrev' /></type_abbrev>
            <aggregationFunction><xsl:value-of select='indivodoc:aggregationFunction/text()' /></aggregationFunction>
            <aggregationFunction_type><xsl:value-of select='indivodoc:aggregationFunction/@type' /></aggregationFunction_type>
            <aggregationFunction_value><xsl:value-of select='indivodoc:aggregationFunction/@value' /></aggregationFunction_value>
            <aggregationFunction_abbrev><xsl:value-of select='indivodoc:aggregationFunction/@abbrev' /></aggregationFunction_abbrev>
            <xsl:if test="indivodoc:textValue">
                <value_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></value_textvalue>
            </xsl:if>
            <xsl:if test="indivodoc:value">
                <value_value><xsl:value-of select='indivodoc:value/text()' /></value_value>
            </xsl:if>
            <xsl:if test="indivodoc:unit">
                <value_unit><xsl:value-of select='indivodoc:unit/text()' /></value_unit>
                <maximumValue_unit_type><xsl:value-of select='indivodoc:unit/@type' /></maximumValue_unit_type>
                <maximumValue_unit_value><xsl:value-of select='indivodoc:unit/@value' /></maximumValue_unit_value>
                <maximumValue_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></maximumValue_unit_abbrev>
            </xsl:if>
        </measurementPlan>
    </xsl:template>

    <xsl:template match="indivodoc:devicePlans">
        <xsl:apply-templates select="indivodoc:devicePlan" />
    </xsl:template>

    <xsl:template match="indivodoc:devicePlan">
        <devicePlan>
            <name><xsl:value-of select='indivodoc:name/text()' /></name>
            <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
            <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
            <type><xsl:value-of select='indivodoc:type/text()' /></type>
            <type_type><xsl:value-of select='indivodoc:type/@type' /></type_type>
            <type_value><xsl:value-of select='indivodoc:type/@value' /></type_value>
            <type_abbrev><xsl:value-of select='indivodoc:type/@abbrev' /></type_abbrev>
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
            <site><xsl:value-of select='indivodoc:site/text()' /></site>
            <site_type><xsl:value-of select='indivodoc:site/@type' /></site_type>
            <site_value><xsl:value-of select='indivodoc:site/@value' /></site_value>
            <site_abbrev><xsl:value-of select='indivodoc:site/@abbrev' /></site_abbrev>
            <instructions><xsl:value-of select='indivodoc:instructions/text()' /></instructions>
        </devicePlan>
    </xsl:template>

    <xsl:template match="indivodoc:medicationPlans">
        <xsl:apply-templates select="indivodoc:medicationPlan" />
    </xsl:template>

    <xsl:template match="indivodoc:medicationPlan">
        <medicationPlan>
            <name><xsl:value-of select='indivodoc:name/text()' /></name>
            <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
            <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
            <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
            <indication><xsl:value-of select='indivodoc:indication/text()' /></indication>
            <xsl:if test="indivodoc:textValue">
                <dose_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></dose_textvalue>
            </xsl:if>
            <xsl:if test="indivodoc:value">
                <dose_value><xsl:value-of select='indivodoc:value/text()' /></dose_value>
            </xsl:if>
            <xsl:if test="indivodoc:unit">
                <dose_unit><xsl:value-of select='indivodoc:unit/text()' /></dose_unit>
                <dose_unit_type><xsl:value-of select='indivodoc:unit/@type' /></dose_unit_type>
                <dose_unit_value><xsl:value-of select='indivodoc:unit/@value' /></dose_unit_value>
                <dose_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></dose_unit_abbrev>
            </xsl:if>
            <route><xsl:value-of select='indivodoc:route/text()' /></route>
            <route_type><xsl:value-of select='indivodoc:route/@type' /></route_type>
            <route_value><xsl:value-of select='indivodoc:route/@value' /></route_value>
            <route_abbrev><xsl:value-of select='indivodoc:route/@abbrev' /></route_abbrev>
            <instructions><xsl:value-of select='indivodoc:instructions/text()' /></instructions>
        </medicationPlan>
    </xsl:template>

</xsl:stylesheet>
