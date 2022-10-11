<?xml version="1.0" encoding="iso-8859-2"?>
<!--Copyright Hiero Software 2022-->
<!--Contact person: HighPriest@github-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="yes" encoding="iso-8859-2"/>    

    <xsl:template match="/">
        <account-history>
            <search>
                <account><xsl:value-of select="account-history/search/account"/></account>
                <xsl:variable name="date-since">
                    <xsl:value-of select="account-history/search/date/@since"/>
                </xsl:variable>
                <xsl:variable name="date-to">
                    <xsl:value-of select="account-history/search/date/@to"/>
                </xsl:variable>
                <date since="{date-since}" to="{date-to}"/>
                <filtering><xsl:value-of select="account-history/search/filtering"/></filtering>
            </search>
            <operations>
                
            </operations>
        </account-history>
    </xsl:template>
</xsl:stylesheet>
