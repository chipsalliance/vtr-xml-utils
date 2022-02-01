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

  <!--
    Strip pack_pattern's from input/output tags on pb_types.
    -->
  <xsl:template match="pb_type/input/pack_pattern"/>
  <xsl:template match="pb_type/output/pack_pattern"/>

  <!--
    Convert
       <pack_pattern name="xxx" type="yyy"
    to
       <pack_pattern name="yyy-xxx"
    -->
  <xsl:template match="pack_pattern/@type"/>
  <xsl:template match="pack_pattern[@type]/@name">
    <xsl:attribute name="name">
      <xsl:value-of select="../@type"/>-<xsl:value-of select="../@name"/>
    </xsl:attribute>
  </xsl:template>
  <xsl:template match="pack_pattern[not(@type)]/@name">
    <xsl:copy />
  </xsl:template>
  <xsl:template match="pack_pattern/*">
    <xsl:copy />
  </xsl:template>

  <!--
    Convert
      <interconnect><direct input="IN" output="OUT"><pack_pattern name="PACK"/></direct></interconnect>
    to
      <interconnect><direct input="IN" output="OUT"><pack_pattern name="PACK" in_port="IN" out_port="OUT"/></direct></interconnect>
    -->
  <xsl:template match="direct[@input and @output]/pack_pattern">
    <xsl:copy>
      <xsl:attribute name="in_port"><xsl:value-of select="../@input" /></xsl:attribute>
      <xsl:attribute name="out_port"><xsl:value-of select="../@output" /></xsl:attribute>
      <xsl:apply-templates select="@*"></xsl:apply-templates>
    </xsl:copy>
    <xsl:apply-templates/>
  </xsl:template>

</xsl:stylesheet>
