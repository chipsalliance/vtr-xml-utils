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

  <!-- template-function: Allow from attribute which gives you a relative to a given pb_type -->
  <xsl:template name="parent-pb_type">
    <xsl:value-of select="ancestor::pb_type[1]/@name"/>
  </xsl:template>

  <xsl:template match="pack_pattern/@in_port">
    <xsl:copy />
  </xsl:template>
  <xsl:template match="pack_pattern/@out_port">
    <xsl:copy />
  </xsl:template>

  <!-- Prefix in_port / out_port values with the parent name. -->
  <xsl:template match="@out_port[not(contains(.,'.'))]">
    <xsl:attribute name="out_port"><xsl:call-template name="parent-pb_type"/>.<xsl:value-of select="."/></xsl:attribute>
  </xsl:template>
  <xsl:template match="@in_port[not(contains(.,'.'))]">
    <xsl:attribute name="in_port"><xsl:call-template name="parent-pb_type"/>.<xsl:value-of select="."/></xsl:attribute>
  </xsl:template>
  <xsl:template match="@port[not(contains(.,'.'))]">
    <xsl:attribute name="port"><xsl:call-template name="parent-pb_type"/>.<xsl:value-of select="."/></xsl:attribute>
  </xsl:template>

</xsl:stylesheet>
