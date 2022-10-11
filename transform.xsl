<?xml version="1.0" encoding="iso-8859-2"?>
<!--Copyright Hiero Software 2022-->
<!--Contact person: HighPriest@github-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="yes" encoding="iso-8859-2"/>    

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
                                <xsl:value-of select="translate(account-history/search/date/@since, '-', '')"/>
                            </DTSTART>
                            <DTEND>
                                <xsl:value-of select="translate(account-history/search/date/@to, '-', '')"/>
                            </DTEND>

                            <xsl:for-each select="account-history/operations/operation">
                                <STMTTRN>
                                    <xsl:variable name="date-id">
                                        <xsl:value-of select="translate(order-date, '-','')"/>
                                    </xsl:variable>
                                    <TRNTYPE><xsl:value-of select="class"/></TRNTYPE>
                                    <DTPOSTED><xsl:value-of select="translate(exec-date, '-', '')"/></DTPOSTED>
                                    <DTUSER><xsl:value-of select="translate(order-date, '-','')"/></DTUSER>
                                    <TRNAMT><xsl:value-of select="amount"/></TRNAMT>
                                    <FITID><xsl:value-of select="concat($date-id, '-', @id)"/></FITID>
                                    <NAME><xsl:value-of select="type"/></NAME>
                                    <EXTDNAME></EXTDNAME>
                                    <MEMO><xsl:value-of select="description"/></MEMO>
                                    <xsl:if test="other-side">
                                        <xsl:if test="class = 'CREDIT'">
                                            <BANKACCTFROM><xsl:value-of select="other-side/account"/></BANKACCTFROM>
                                            <BANKACCTTO><xsl:value-of select="/account-history/search/account"/></BANKACCTTO>
                                        </xsl:if>
                                        <xsl:if test="class = 'DEBIT'">
                                            <BANKACCTTO><xsl:value-of select="other-side/account"/></BANKACCTTO>
                                            <BANKACCTFROM><xsl:value-of select="/account-history/search/account"/></BANKACCTFROM>
                                        </xsl:if>
                                    </xsl:if>
                                </STMTTRN>
                            </xsl:for-each>
                        </BANKTRANLIST>
                    </STMTRS>
                </STMTTRNRS>

            </BANKMSGSRSV1>
        </OFX>
    </xsl:template>
</xsl:stylesheet>
