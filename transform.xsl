<?xml version="1.0" encoding="ISO-8859-2"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="yes" encoding="ISO-8859-2"/>    

    <xsl:template match="/">
        <OFX>
            <BANKMSGSRSV1>
                <STMTTRNRS>
                    <TRNUID>0</TRNUID>
                    <STMTRS>
                        <CURDEF>PLN</CURDEF>
                        <BANKACCTFROM>
                            <BANKID>Inteligo</BANKID>
                            <ACCTID><xsl:value-of select="account-history/search/account"/></ACCTID>
                            <ACCTTYPE>CHECKING</ACCTTYPE>
                        </BANKACCTFROM>
                        <BANKTRANLIST>
                            <DTSTART>
                                <xsl:value-of select="account-history/search/date">
                                    <xsl:value-of select="@since"/>
                                </xsl:value-of>
                            </DTSTART>

                            <xsl:for-each select="account-history/operations/operation">
                                <STMTTRN>
                                    <TRNTYPE><xsl:value-of select="class"/></TRNTYPE>
                                    <xsl:variable name="exec-date">
                                        <xsl:value-of select="exec-date"/>
                                    </xsl:variable>
                                    <DTPOSTED><xsl:value-of select="translate($exec-date, '-', '')"/></DTPOSTED>
                                    <xsl:variable name="order-date">
                                        <xsl:value-of select="order-date"/>
                                    </xsl:variable>
                                    <DTUSER><xsl:value-of select="translate($order-date, '-','')"/></DTUSER>
                                    <TRNAMT><xsl:value-of select="amount"/></TRNAMT>
                                    <FITID><xsl:value-of select="@id"/></FITID>
                                    <xsl:variable name="type">
                                        <xsl:value-of select="type"/>
                                    </xsl:variable>
                                    <xsl:variable name="desc">
                                        <xsl:value-of select="description"/>
                                    </xsl:variable>
                                    <NAME><xsl:value-of select="$type"/></NAME>
                                    <MEMO><xsl:value-of select="$desc"/></MEMO>
                                </STMTTRN>
                            </xsl:for-each>
                        </BANKTRANLIST>
                    </STMTRS>
                </STMTTRNRS>

            </BANKMSGSRSV1>
        </OFX>
    </xsl:template>
</xsl:stylesheet>
