<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:MedicationOrder">
    <facts>
      <fact>
        <xsl:if test="indivodoc:name">
	        <name><xsl:value-of select='indivodoc:name/text()' /></name>
	        <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
	        <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
	        <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
        </xsl:if>
        <orderType><xsl:value-of select='indivodoc:orderType/text()' /></orderType>
        <orderedBy><xsl:value-of select='indivodoc:orderedBy/text()' /></orderedBy>
        <dateOrdered><xsl:value-of select='indivodoc:dateOrdered/text()' /></dateOrdered>
        <xsl:if test="indivodoc:dateExpires">
          <dateExpires><xsl:value-of select='indivodoc:dateExpires/text()' /></dateExpires>
        </xsl:if>
        <xsl:if test="indivodoc:indication">
          <indication><xsl:value-of select='indivodoc:indication/text()' /></indication>
        </xsl:if>
        <xsl:apply-templates select='indivodoc:amountOrdered' />
        <xsl:if test="indivodoc:refills">
          <refills><xsl:value-of select='indivodoc:refills/text()' /></refills>
        </xsl:if>
        <xsl:if test="indivodoc:substitutionPermitted">
          <substitutionPermitted><xsl:value-of select='indivodoc:substitutionPermitted/text()' /></substitutionPermitted>
        </xsl:if>
        <xsl:if test="indivodoc:instructions">
          <instructions><xsl:value-of select='indivodoc:instructions/text()' /></instructions>
        </xsl:if>        
      </fact>
    </facts>
  </xsl:template>

  <xsl:template match="indivodoc:amountOrdered">
    <xsl:if test="indivodoc:textValue">
      <amountOrdered_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></amountOrdered_textvalue>
    </xsl:if>
    <xsl:if test="indivodoc:value">
      <amountOrdered_value><xsl:value-of select='indivodoc:value/text()' /></amountOrdered_value>
    </xsl:if>
    <xsl:if test="indivodoc:unit">
      <amountOrdered_unit>
        <xsl:value-of select='indivodoc:unit/text()' />
      </amountOrdered_unit>
      <amountOrdered_unit_type><xsl:value-of select='indivodoc:unit/@type' /></amountOrdered_unit_type>
      <amountOrdered_unit_value><xsl:value-of select='indivodoc:unit/@value' /></amountOrdered_unit_value>
      <amountOrdered_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></amountOrdered_unit_abbrev>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
