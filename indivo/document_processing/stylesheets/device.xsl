<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:Device">
    <facts>
      <fact>
        <name><xsl:value-of select='indivodoc:name/text()' /></name>
        <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
        <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
        <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
        <xsl:if test="indivodoc:id">
          <identity><xsl:value-of select='indivodoc:id/text()' /></identity>
          <identity_type><xsl:value-of select='indivodoc:id/@type' /></identity_type>
          <identity_value><xsl:value-of select='indivodoc:id/@value' /></identity_value>
          <identity_abbrev><xsl:value-of select='indivodoc:id/@abbrev' /></identity_abbrev>
        </xsl:if>
        <xsl:if test="indivodoc:type">
          <type><xsl:value-of select='indivodoc:type/text()' /></type>
          <type_type><xsl:value-of select='indivodoc:type/@type' /></type_type>
          <type_value><xsl:value-of select='indivodoc:type/@value' /></type_value>
          <type_abbrev><xsl:value-of select='indivodoc:type/@abbrev' /></type_abbrev>
        </xsl:if>
        <xsl:if test="indivodoc:indication">
          <indication><xsl:value-of select='indivodoc:indication/text()' /></indication>
        </xsl:if>
        <xsl:if test="indivodoc:vendor">
          <vendor><xsl:value-of select='indivodoc:vendor/text()' /></vendor>
          <vendor_type><xsl:value-of select='indivodoc:vendor/@type' /></vendor_type>
          <vendor_value><xsl:value-of select='indivodoc:vendor/@value' /></vendor_value>
          <vendor_abbrev><xsl:value-of select='indivodoc:vendor/@abbrev' /></vendor_abbrev>
        </xsl:if>
        <xsl:if test="indivodoc:description">
          <description><xsl:value-of select='indivodoc:description/text()' /></description>
        </xsl:if>
        <xsl:if test="indivodoc:specification">
          <specification><xsl:value-of select='indivodoc:specification/text()' /></specification>
        </xsl:if>
        <xsl:if test="indivodoc:certification">
          <certification><xsl:value-of select='indivodoc:certification/text()' /></certification>
        </xsl:if>
      </fact>
    </facts>
  </xsl:template>
</xsl:stylesheet>
