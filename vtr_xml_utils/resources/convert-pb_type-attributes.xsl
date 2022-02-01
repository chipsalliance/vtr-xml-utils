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

  <xsl:template match="pb_type">
    <xsl:copy>
      <!--
        Convert
          <pb_type><blif_model>XXX</blif_model></pb_type>
        to
          <pb_type blif_model="XXX"></pb_type>
        -->
      <xsl:if test="blif_model">
        <xsl:attribute name="blif_model"><xsl:value-of select="blif_model/text()"/></xsl:attribute>
      </xsl:if>
      <!-- Inherit 'num_pb' attribute from pb_array elements -->
      <xsl:if test="parent::pb_array/@num_pb">
        <xsl:attribute name="num_pb"><xsl:value-of select="parent::pb_array/@num_pb"/></xsl:attribute>
      </xsl:if>
      <!--
        Convert
          <pb_type><pb_class>XXX</pb_class></pb_type>
        to
          <pb_type class="XXX"></pb_type>
        -->
      <xsl:if test="pb_class">
        <xsl:attribute name="class"><xsl:value-of select="pb_class/text()"/></xsl:attribute>
      </xsl:if>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates select="node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="pb_type/blif_model"/>
  <xsl:template match="pb_type/pb_class"/>

  <!-- Copy pb_type elements out of pb_array elements -->
  <xsl:template match="pb_array">
    <xsl:apply-templates/>
  </xsl:template>

</xsl:stylesheet>
