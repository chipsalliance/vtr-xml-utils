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
  <xsl:output method="xml" indent="yes"/>
  <xsl:strip-space elements="*"/>

  <xsl:template match="@*">
    <xsl:copy/>
  </xsl:template>

  <xsl:template match="*">
    <xsl:copy>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="text()|processing-instruction()">
    <xsl:copy>
      <xsl:apply-templates select="text()|processing-instruction()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:param name="strip_comments" select="''" />
  <xsl:template match="comment()">
    <xsl:choose>
      <xsl:when test="$strip_comments"></xsl:when>
      <xsl:otherwise><xsl:copy /></xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
