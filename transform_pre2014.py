#!/bin/python3
# Copyright 2022 Łukasz Herok, HighPriest@Hiero Software
# Contact person: HighPriest@github

import getopt
import os
import sys
import lxml.etree as et
import re
import codecs


def transform(inputfilename):
    dom = et.parse(inputfilename)
    xslt = et.parse('transform.xsl')
    output = et.XSLT(xslt)

    docinfo = dom.docinfo
    print(docinfo.encoding)

    return output(dom)


def _przelew_extract(memo):
    m = re.match(r"(.*) Nr rach.: (.*) Tytuł: (.*) Data waluty: (.*)", memo.text)
    if (m):
        kto = m.group(1)
        konto = m.group(2)
        co = m.group(3)
    else:
        m = re.match(r"(Nr telefonu: .*) (Kod doładowania.*) Data waluty: (.*)", memo.text)
        konto = 'None'
        kto = m.group(1)
        co = m.group(2)
    return konto, kto, co


def _karta_extract(memo):
    m = re.match(r"Kwota operacji: (.*) PLN (?:(?:Kwota rozliczeniowa:) (\S*) (\S*) (?:Data przetworzenia:) (\S*) (?:Kurs walutowy:) (\S*))?(.*) Data wykonania: (.*) Karta nr: (.*) Data waluty: (.*)", memo.text)
    kwota = m.group(1)
    kwota_obca = m.group(2)
    waluta_symbol = str(m.group(3))
    waluta_data = m.group(4)
    waluta_kurs = m.group(5) 
    kto = m.group(6)
    data_zlecenia = m.group(7)
    data_wykonania = m.group(9)
    karta = m.group(8)
    return kto, karta, kwota_obca, waluta_symbol


def _cleanup_desc(name, extname, memo):
    if name.text == 'Przelew z rachunku' or name.text == 'Zlecenie stałe':
        konto, kto, co = _przelew_extract(memo)
        extname.text = co + ', dla: ' + kto + '; Nr Konta: ' + konto
        memo.text = co + ', dla: ' + kto
        name.text = name.text + ', dla: ' + kto
    elif name.text == 'Przelew na rachunek':
        konto, kto, co = _przelew_extract(memo)
        extname.text = co + ', od: ' + kto + '; Nr Konta: ' + konto
        memo.text = co + ', od: ' + kto
        name.text = name.text + ', od: ' + kto
    elif name.text == 'Płatność kartą' or name.text == 'Wypłata z bankomatu':
        kto, karta, kwota_obca, waluta_symbol = _karta_extract(memo)
        if waluta_symbol != 'None':
            extname.text = 'Karta: ' + karta + ', w: ' + kto + '; Kwota: ' + kwota_obca + ' ' + waluta_symbol
            memo.text = 'Karta: ' + karta + ', w: ' + kto
            name.text = name.text + ', w: ' + kto
        else:
            extname.text = 'Karta: ' + karta + ', w: ' + kto
            memo.text = name.text + " " + karta + ', w: ' + kto
            name.text = name.text + ", w: " + kto


def cleanup(newdom):
    for el in newdom.iter("STMTTRN"):
        name = el.find('NAME')
        extname = el.find('EXTDNAME')
        memo = el.find('MEMO')
      
        try:
            _cleanup_desc(name, extname, memo)
        except:
            print("Nie udało się rozkodować")
            print(name.text)
            print(extname.text)
            print(memo.text) 

def conv_encoding(encoding, outputfilename):
    BLOCKSIZE = 1048576 # or some other, desired size in bytes
    with codecs.open('_inteligo_8859.ofx', "r", encoding) as sourceFile:
        with codecs.open(outputfilename, "w", "utf-8") as targetFile:
            while True:
                contents = sourceFile.read(BLOCKSIZE)
                if not contents:
                    break
                targetFile.write(contents)
        print("The dom has been converted from: "+ sourceFile.encoding + " to: "+ targetFile.encoding)
    if os.path.exists("_inteligo_8859.ofx"):
        os.remove("_inteligo_8859.ofx")


def main(argv):
    inputfilename = 'historia_pre2014.xml'
    outputfilename = 'inteligo.ofx'
    
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["help","ifile","in","input","ofile","out","output"])
    except getopt.GetoptError:
        print("transform.py -i <inputfile> -o <outputfilename>\n"+
              "             -h, --help for more information\n")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print("transform.py -i <inputfile> -o <outputfilename>\n" + 
                  "             -i, --ifile, --in, --input <inputfile>\n" +
                  "                 File which you want to import, but some IDs have already been used and transactions are not imported\n" +
                  "             -o, --ofile, --out, --output <outputfilename>\n"+
                  "                 File which will be created with new IDs\n")
            sys.exit()
        elif opt in ("-i", "--ifile", "--in", "--input"):
            inputfilename = arg
        elif opt in ("-o", "--ofile", "--out", "--output"):
            if arg.split(".")[1] & arg.split(".")[-1] == ".ofx":
                outputfilename = arg
            else:
                outputfilename = arg + ".ofx"
    print("Input file is: " + inputfilename)
    print("Output file is: " + outputfilename)


    encoding, newdom = transform(inputfilename)
    cleanup(newdom)
    newdom.write('_inteligo_8859.ofx', pretty_print=True, encoding=encoding)
    conv_encoding(encoding, outputfilename)

    print(
        "Inteligo->GnuCash  Copyright (C) 2022  HighPriest@Hiero Software\n" +
        "This program comes with ABSOLUTELY NO WARRANTY\n" +
        "This is free software, and you are welcome to redistribute it, under certain conditions;"
    )

if __name__ == '__main__':
    main(sys.argv[1:])

"""
    Copyright (C) 2022  Łukasz Herok, HighPriest@Hiero Software

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
