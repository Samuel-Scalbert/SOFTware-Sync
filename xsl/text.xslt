<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  version="3.0"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  exclude-result-prefixes="#all"
  expand-text="yes">

  <xsl:template match="p">
    <xsl:iterate select="$json-doc?*[?type = 'software']">
      <xsl:param name="p" select="."/>
      <xsl:on-completion select="$p"/>
      <xsl:if test="contains($p, ?context)">
        <xsl:variable name="transformed-p" as="element(p)">
          <xsl:apply-templates select="$p" mode="process">
            <xsl:with-param name="software" select="." tunnel="yes"/>
          </xsl:apply-templates>
        </xsl:variable>
        <xsl:next-iteration>
          <xsl:with-param name="p" select="$transformed-p"/>
        </xsl:next-iteration>
      </xsl:if>
    </xsl:iterate>
  </xsl:template>

  <xsl:mode name="process" on-no-match="shallow-copy"/>

  <xsl:template mode="process" match="p//text()">
    <xsl:param name="software" tunnel="yes" as="map(*)"/>
    <xsl:choose>
      <xsl:when test="contains($software?context, .) and contains(., $software?software-name?normalizedForm)">
        <xsl:apply-templates select="analyze-string(., $software?software-name?normalizedForm)" mode="wrap"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:next-match/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template mode="wrap" match="*:match">
    <software>{.}</software>
  </xsl:template>


  <xsl:output method="xml" indent="no"/>

  <xsl:mode on-no-match="shallow-copy"/>

  <xsl:param name="json-doc" select="./data/json_files/PMC3130168.json"/>

</xsl:stylesheet>