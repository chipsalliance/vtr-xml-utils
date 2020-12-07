<?xml version="1.0"?>
<!-- 
 Copyright (C) 2020  The SymbiFlow Authors.

 Use of this source code is governed by a ISC-style
 license that can be found in the LICENSE file or at
 https://opensource.org/licenses/ISC

 SPDX-License-Identifier:   ISC
-->
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
