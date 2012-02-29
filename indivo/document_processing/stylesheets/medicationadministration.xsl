<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:MedicationAdministration">
    <facts>
      <fact>
        <name><xsl:value-of select='indivodoc:name/text()' /></name>
        <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
        <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
        <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
        <reportedBy><xsl:value-of select='indivodoc:reportedBy/text()' /></reportedBy>
        <dateReported><xsl:value-of select='indivodoc:dateReported/text()' /></dateReported>
        <xsl:if test="indivodoc:dateAdministered">
          <dateAdministered><xsl:value-of select='indivodoc:dateAdministered/text()' /></dateAdministered>
        </xsl:if>
        <xsl:if test="indivodoc:amountAdministered">
          <xsl:apply-templates select='indivodoc:amountAdministered' />
        </xsl:if>
        <xsl:if test="indivodoc:amountRemaining">
          <xsl:apply-templates select='indivodoc:dateAdministered' />
        </xsl:if>
      </fact>
    </facts>
  </xsl:template>
  <xsl:template match="indivodoc:amountAdministered">
    <xsl:if test="indivodoc:textValue">
      <amountAdministered_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></amountAdministered_textvalue>
    </xsl:if>
    <xsl:if test="indivodoc:value">
      <amountAdministered_value><xsl:value-of select='indivodoc:value/text()' /></amountAdministered_value>
    </xsl:if>
    <xsl:if test="indivodoc:unit">
      <amountAdministered_unit>
        <xsl:value-of select='indivodoc:unit/text()' />
      </amountAdministered_unit>
      <amountAdministered_unit_type><xsl:value-of select='indivodoc:unit/@type' /></amountAdministered_unit_type>
      <amountAdministered_unit_value><xsl:value-of select='indivodoc:unit/@value' /></amountAdministered_unit_value>
      <amountAdministered_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></amountAdministered_unit_abbrev>
    </xsl:if>
  </xsl:template>
  <xsl:template match="indivodoc:amountRemaining">
    <xsl:if test="indivodoc:textValue">
      <amountRemaining_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></amountRemaining_textvalue>
    </xsl:if>
    <xsl:if test="indivodoc:value">
      <amountRemaining_value><xsl:value-of select='indivodoc:value/text()' /></amountRemaining_value>
    </xsl:if>
    <xsl:if test="indivodoc:unit">
      <amountRemaining_unit>
        <xsl:value-of select='indivodoc:unit/text()' />
      </amountRemaining_unit>
      <amountRemaining_unit_type><xsl:value-of select='indivodoc:unit/@type' /></amountRemaining_unit_type>
      <amountRemaining_unit_value><xsl:value-of select='indivodoc:unit/@value' /></amountRemaining_unit_value>
      <amountRemaining_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></amountRemaining_unit_abbrev>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>
