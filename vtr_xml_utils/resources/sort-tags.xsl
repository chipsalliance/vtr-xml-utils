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
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <xsl:include href="identity.xsl" />

 <!-- Sort <pb_type><clock> by "name" attribute -->
 <!-- Sort <pb_type><input> by "name" attribute -->
 <!-- Sort <pb_type><output> by "name" attribute -->
 <xsl:template match="pb_type">
  <xsl:copy>
   <xsl:apply-templates select="@*"/>
   <xsl:apply-templates select="clock">
    <xsl:sort select="@name" order="ascending"/>
   </xsl:apply-templates>
   <xsl:apply-templates select="input">
    <xsl:sort select="@name" order="ascending"/>
   </xsl:apply-templates>
   <xsl:apply-templates select="output">
    <xsl:sort select="@name" order="ascending"/>
   </xsl:apply-templates>
   <xsl:apply-templates select="delay_constant">
    <xsl:sort select="concat(@out_port,@in_port)" order="ascending"/>
   </xsl:apply-templates>
   <xsl:apply-templates select="pb_type">
    <xsl:sort select="@name" order="ascending"/>
   </xsl:apply-templates>
   <xsl:apply-templates select="*[not(self::clock or self::input or self::output or self::pb_type or self::delay_constant)]"/>
  </xsl:copy>
 </xsl:template>
 <!-- Sort <interconnect><XXX> tags by output - direct first then muxes, finally input -->
 <xsl:template match="interconnect">
  <xsl:copy>
   <xsl:apply-templates>
    <xsl:sort select="concat(@output, name(), @input)" order="ascending"/>
   </xsl:apply-templates>
  </xsl:copy>
 </xsl:template>

</xsl:stylesheet>
