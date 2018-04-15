#!/bin/python3

import lxml.etree as et
import re
import codecs

def transform():
    dom = et.parse('historia.xml')
    xslt = et.parse('transform.xsl')
    transform = et.XSLT(xslt)

    docinfo = dom.docinfo
    print(docinfo.encoding)

    return transform(dom)

def _cleanup_name(name):
    name.text = name.text.replace('Przelew z rachunku', 'Przelew> ')
    name.text = name.text.replace('Przelew na rachunek', 'Przelew< ')
    name.text = name.text.replace('Płatność kartą', 'Karta ')
    name.text = name.text.replace('Wypłata z bankomatu', 'Bankomat ')
    name.text = name.text.replace('Zlecenie stałe', 'Zlecenie stałe ')

def _przelew_extract(memo):
    m = re.match(r".*Dane adr\. rach\. przeciwst\.: (.*)Tytuł: (.*)Data waluty", memo.text)
    kto = m.group(1)[:30]
    co = m.group(2).lower()
    m = re.match(r"(.*)( ul\.| UL\.|UL\. )", kto)
    if m:
        kto = m.group(1)
    return kto, co

def _karta_extract(memo):
    m = re.match(r".*Kraj: \w+ Miasto: (.*) Adres: (.*) Data wykonania: (.*) Numer referencyjny:(.*)Numer karty: (.*) Data waluty", memo.text)
    miasto = m.group(1)
    kto = m.group(2)
    tms = m.group(3)
    karta = m.group(5)
    if karta == '* *999':
        karta = 'Karta1'
    if karta == '* *999':
        karta = 'Karta2'
    return miasto, kto, tms, karta

def _cleanup_desc(name, memo):
    if name.text == 'Przelew> ':
        kto, co = _przelew_extract(memo)
        name.text = name.text + kto + ': ' + co
        memo.text = ''
    if name.text == 'Przelew< ':
        kto, co = _przelew_extract(memo)
        name.text = name.text + kto + ': ' + co
        memo.text = ''
    if name.text == 'Karta ':
        miasto, kto, tms, karta = _karta_extract(memo)
        name.text = name.text + karta + ", " + miasto + " " + kto
        memo.text = tms 
    if name.text == 'Bankomat ':
        miasto, kto, tms, karta = _karta_extract(memo)
        name.text = name.text + karta + ", " + miasto + " " + kto + ", " + tms
        memo.text = ''
    if name.text == 'Zlecenie stałe ':
        kto, co = _przelew_extract(memo)
        name.text = name.text + kto + ': ' + co
        memo.text = ''


def cleanup(newdom):
    for el in newdom.iter("STMTTRN"):
        name = el.find('NAME')
        memo = el.find('MEMO')

        _cleanup_name(name)        
        try:
            _cleanup_desc(name, memo)
        except:
            print("Nie udało się rozkodować")
            print(name.text)
            print(memo.text) 

        #print(name.text)
        #print(memo.text) 

def conv_encoding():
    BLOCKSIZE = 1048576 # or some other, desired size in bytes
    with codecs.open('_inteligo_8859.ofx', "r", "iso-8859-2") as sourceFile:
        with codecs.open('inteligo2.ofx', "w", "utf-8") as targetFile:
            while True:
                contents = sourceFile.read(BLOCKSIZE)
                if not contents:
                    break
                targetFile.write(contents)

if __name__ == '__main__':

    newdom = transform()
    cleanup(newdom)
    newdom.write('_inteligo_8859.ofx', pretty_print=True, encoding='iso-8859-2')
    conv_encoding()


