<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:VitalSign">
    <facts>
      <fact>
        <name><xsl:value-of select='indivodoc:name/text()' /></name>
        <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
        <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
        <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
        <measuredBy><xsl:value-of select='indivodoc:measuredBy/text()' /></measuredBy>
        <dateMeasuredStart><xsl:value-of select='indivodoc:dateMeasuredStart/text()' /></dateMeasuredStart>
        <xsl:if test="indivodoc:dateMeasuredEnd">        
          <dateMeasuredEnd><xsl:value-of select='indivodoc:dateMeasuredEnd/text()' /></dateMeasuredEnd>
        </xsl:if>
        <xsl:if test="indivodoc:result">        
          <xsl:apply-templates select='indivodoc:result' /> 
        </xsl:if>
        <xsl:if test="indivodoc:site">        
          <site><xsl:value-of select='indivodoc:site/text()' /></site>
        </xsl:if>
        <xsl:if test="indivodoc:position">        
          <position><xsl:value-of select='indivodoc:position/text()' /></position>
        </xsl:if>
        <xsl:if test="indivodoc:technique">        
          <technique><xsl:value-of select='indivodoc:technique/text()' /></technique>
        </xsl:if>
        <xsl:if test="indivodoc:comments">        
          <comments><xsl:value-of select='indivodoc:comments/text()' /></comments>
        </xsl:if>
      </fact>
    </facts>
  </xsl:template>


  <xsl:template match="indivodoc:result">
    <xsl:if test="indivodoc:textValue">
      <result_textvalue><xsl:value-of select='indivodoc:textValue/text()' /></result_textvalue>
    </xsl:if>
    <xsl:if test="indivodoc:value">
      <result_value><xsl:value-of select='indivodoc:value/text()' /></result_value>
    </xsl:if>
    <xsl:if test="indivodoc:unit">
      <result_unit>
        <xsl:value-of select='indivodoc:unit/text()' />
      </result_unit>
      <result_unit_type><xsl:value-of select='indivodoc:unit/@type' /></result_unit_type>
      <result_unit_value><xsl:value-of select='indivodoc:unit/@value' /></result_unit_value>
      <result_unit_abbrev><xsl:value-of select='indivodoc:unit/@abbrev' /></result_unit_abbrev>
    </xsl:if>
  </xsl:template>


</xsl:stylesheet>
