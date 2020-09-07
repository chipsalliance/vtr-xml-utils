<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:include href="identity.xsl" />

  <!-- Remove duplicate model nodes -->
  <xsl:key name="model-by-name" match="model" use="@name" />
  <xsl:template match="models">
    <models>
      <xsl:for-each select="model[count(. | key('model-by-name', @name)[1]) = 1]">
        <xsl:copy>
          <xsl:attribute name="name"><xsl:value-of select="@name"/></xsl:attribute>
	  <xsl:if test="@never_prune='true'">
            <xsl:attribute name="never_prune"><xsl:value-of select="@never_prune"/></xsl:attribute>
	  </xsl:if>
          <xsl:apply-templates/>
        </xsl:copy>
      </xsl:for-each>
    </models>
  </xsl:template>

</xsl:stylesheet>
