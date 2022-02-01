<?xml version="1.0"?>
<!-- 
 Copyright 2020-2022 F4PGA Authors

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

 SPDX-License-Identifier: Apache-2.0
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
