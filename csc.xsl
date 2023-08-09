<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
            <head>
                <title><xsl:value-of select = "comic/title" /></title>
            </head>
            <body>
                <span style="font-size:.25in;"><b><xsl:value-of select = "comic/title" /></b></span><br />
                <span><xsl:value-of select = "comic/author" />&#60;<xsl:value-of select="comic/email" />&#62;</span><br />
                <span>Draft:<xsl:value-of select = "comic/draft" /></span><br />
                <span><xsl:value-of select = "comic/date" /></span><hr />
                <xsl:apply-templates select="//page"/>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template match="page">
        <h2>Page <xsl:value-of select="@num"/></h2>
        <xsl:apply-templates select="panel"/><hr />
    </xsl:template>
    
    <xsl:template match="panel">
        <div> 
            <u>Panel <xsl:value-of select="@num"/></u>
            <xsl:apply-templates select="character | narrator | action | dialog"/>
        </div>
    </xsl:template>
    
    <xsl:template match="character">
        <p style='margin-left:1in;'><strong><xsl:value-of select="@name"/>:</strong><br />
            <xsl:if test="mood/text()">
        yes
        </xsl:if>
<!-- none of t his worked -->
        <xsl:if test="mood/*">
        has elements
        </xsl:if>
        <xsl:if test="mood[not(node())]">
        is empty
        </xsl:if>
        <xsl:if test="not(mood)">
        no node1
        </xsl:if>
            <xsl:attribute name = "xsl:nil">true</xsl:attribute><xsl:value-of select = "(@mood)" /><br /><xsl:value-of select="normalize-space(.)"/></p>
    </xsl:template>
    
    <xsl:template match="narrator">
        <p style='margin-left:1in;'><strong>narrator:</strong><br /><xsl:value-of select="normalize-space(.)"/></p>
    </xsl:template>
    <xsl:template match="action">
        <p><xsl:value-of select="normalize-space(.)"/></p>
    </xsl:template>
    <xsl:template match="dialog">
        <p><xsl:value-of select="normalize-space(.)"/></p>
    </xsl:template>
</xsl:stylesheet>
