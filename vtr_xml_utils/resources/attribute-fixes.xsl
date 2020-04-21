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

  <!-- Strip xml:base attribute -->
  <xsl:template match="@xml:base"/>

  <!-- Normalize space around attributes on a tag -->
  <xsl:template match="@*">
    <xsl:copy>
      <xsl:value-of select="normalize-space( . )" />
    </xsl:copy>
    <xsl:apply-templates/>
  </xsl:template>

  <!-- Sort the attributes by name -->
  <xsl:template match="*">
    <xsl:copy>
      <xsl:for-each select="@*[name()!='xml:base']">
        <xsl:sort select="name( . )"/>
        <xsl:attribute name="{local-name()}"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>
      </xsl:for-each>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
