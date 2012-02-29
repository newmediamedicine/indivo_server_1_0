<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:MedicationFill">
    <facts>
      <fact>
        <name><xsl:value-of select='indivodoc:name/text()' /></name>
        <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
        <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
        <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
        <filledBy><xsl:value-of select='indivodoc:filledBy/text()' /></filledBy>
        <dateFilled><xsl:value-of select='indivodoc:dateFilled/text()' /></dateFilled>
        <xsl:apply-templates select='indivodoc:amountFilled' />
        <xsl:if test="indivodoc:ndc">
          <ndc><xsl:value-of select='indivodoc:ndc/text()' /></ndc>
          <ndc_type><xsl:value-of select='indivodoc:ndc/@type' /></ndc_type>
          <ndc_value><xsl:value-of select='indivodoc:ndc/@value' /></ndc_value>
          <ndc_abbrev><xsl:value-of select='indivodoc:ndc/@abbrev' /></ndc_abbrev>
        </xsl:if>
        <xsl:if test="indivodoc:fillSequenceNumber">
          <fillSequenceNumber><xsl:value-of select='indivodoc:fillSequenceNumber/text()' /></fillSequenceNumber>
        </xsl:if>
        <xsl:if test="indivodoc:lotNumber">
          <lotNumber><xsl:value-of select='indivodoc:lotNumber/text()' /></lotNumber>
        </xsl:if>
        <xsl:if test="indivodoc:refillsRemaining">
          <refillsRemaining><xsl:value-of select='indivodoc:refillsRemaining/text()' /></refillsRemaining>
        </xsl:if>
        <xsl:if test="indivodoc:instructions">
          <instructions><xsl:value-of select='indivodoc:instructions/text()' /></instructions>
        </xsl:if>        
      </fact>
    </facts>
  </xsl:template>

  <xsl:template match="indivodoc:amountFilled">
    <xsl:if test="indivodoc:textValue">
      <amountFilled_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></amountFilled_textvalue>
    </xsl:if>
    <xsl:if test="indivodoc:value">
      <amountFilled_value><xsl:value-of select='indivodoc:value/text()' /></amountFilled_value>
    </xsl:if>
    <xsl:if test="indivodoc:unit">
      <amountFilled_unit>
        <xsl:value-of select='indivodoc:unit/text()' />
      </amountFilled_unit>
      <amountFilled_unit_type><xsl:value-of select='indivodoc:unit/@type' /></amountFilled_unit_type>
      <amountFilled_unit_value><xsl:value-of select='indivodoc:unit/@value' /></amountFilled_unit_value>
      <amountFilled_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></amountFilled_unit_abbrev>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
