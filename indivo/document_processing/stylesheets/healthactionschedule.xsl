<?xml version='1.0' encoding='ISO-8859-1'?>
<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:indivodoc="http://indivo.org/vocab/xml/documents#"> 
  <xsl:output method = "xml" indent = "yes" />  
  <xsl:template match="indivodoc:HealthActionSchedule">
    <facts>
      <fact>
        <name><xsl:value-of select='indivodoc:name/text()' /></name>
        <name_type><xsl:value-of select='indivodoc:name/@type' /></name_type>
        <name_value><xsl:value-of select='indivodoc:name/@value' /></name_value>
        <name_abbrev><xsl:value-of select='indivodoc:name/@abbrev' /></name_abbrev>
        <scheduledBy><xsl:value-of select='indivodoc:scheduledBy/text()' /></scheduledBy>
        <dateScheduled><xsl:value-of select='indivodoc:dateScheduled/text()' /></dateScheduled>
        <dateStart><xsl:value-of select='indivodoc:dateStart/text()' /></dateStart>
        <xsl:if test="indivodoc:dateEnd">
          <dateEnd><xsl:value-of select='indivodoc:dateEnd/text()' /></dateEnd>
        </xsl:if>
        <xsl:if test="indivodoc:recurrenceRule">
          <xsl:apply-templates select="indivodoc:recurrenceRule" />
        </xsl:if>
        <instructions><xsl:value-of select='indivodoc:instructions/text()' /></instructions>
      </fact>
    </facts>
  </xsl:template>

  <xsl:template match="indivodoc:recurrenceRule">
    <recurrenceRule_frequency><xsl:value-of select='indivodoc:frequency/text()' /></recurrenceRule_frequency>
    <recurrenceRule_frequency_type><xsl:value-of select='indivodoc:frequency/@type' /></recurrenceRule_frequency_type>
    <recurrenceRule_frequency_value><xsl:value-of select='indivodoc:frequency/@value' /></recurrenceRule_frequency_value>
    <recurrenceRule_frequency_abbrev><xsl:value-of select='indivodoc:frequency/@abbrev' /></recurrenceRule_frequency_abbrev>
    <xsl:if test="indivodoc:interval">
      <recurrenceRule_interval><xsl:value-of select='indivodoc:interval/text()' /></recurrenceRule_interval>
      <recurrenceRule_interval_type><xsl:value-of select='indivodoc:interval/@type' /></recurrenceRule_interval_type>
      <recurrenceRule_interval_value><xsl:value-of select='indivodoc:interval/@value' /></recurrenceRule_interval_value>
      <recurrenceRule_interval_abbrev><xsl:value-of select='indivodoc:interval/@abbrev' /></recurrenceRule_interval_abbrev>
    </xsl:if>
    <xsl:if test="indivodoc:count">
      <recurrenceRule_count><xsl:value-of select='indivodoc:count/text()' /></recurrenceRule_count>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>
