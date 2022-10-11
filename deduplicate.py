#!/bin/python3
# Copyright 2022 Łukasz Herok, HighPriest@Hiero Software
# Contact person: HighPriest@github
import getopt
import os
import sys
import lxml.etree as et
import codecs

def deduplicate(inputfilename: str, sourcefilename: str):
    inputdom = et.parse(inputfilename)
    sourcedom = et.parse(sourcefilename)
    transform = et.XSLT(et.parse('deduplicate.xsl'))
    outputdom = transform(sourcedom)
    print("Input dom is encoded in: " + inputdom.docinfo.encoding)
    print("Source dom is encoded in: " + sourcedom.docinfo.encoding)
    print("Output dom is encoded in: " + outputdom.docinfo.encoding)

    for operation in inputdom.xpath("//account-history/operations/operation/@id"):
        if operation in sourcedom.xpath("//account-history/operations/operation/@id"):
            print("Transaction id " + operation + " already exists in input file")
            outputdom.xpath("//account-history/operations")[0].append(operation.getparent())
    
    return outputdom

def transform(dedupeddom):
    xslt = et.parse('transform.xsl')
    transform = et.XSLT(xslt)

    print("Deduped dom is now encoded in: " + dedupeddom.docinfo.encoding)

    return dedupeddom.docinfo.encoding, transform(dedupeddom)


def cleanup(newdom):
    from cleanup_functions import _cleanup_desc
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
        print("Deduped dom has been converted from: "+ sourceFile.encoding + " to: "+ targetFile.encoding)
    if os.path.exists("_inteligo_8859.ofx"):
        os.remove("_inteligo_8859.ofx")


def main(argv):
    inputfilename = 'historia.xml'
    sourcefilename = 'historia_old.xml'
    outputfilename = 'inteligo.ofx'
    
    try:
        opts, args = getopt.getopt(argv,"hi:s:o:",["help","ifile","in","input","sfile","source","ofile","out","output"])
    except getopt.GetoptError:
        print("transform.py -i <inputfile> -s <sourcefile> -o <outputfilename>\n"+
              "             -h, --help for more information\n")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print("transform.py -i <inputfile> -s <sourcefile> -o <outputfilename>\n" + 
                  "             -i, --ifile, --in, --input <inputfile>\n" +
                  "                 File which you want to import, but some IDs have already been used and transactions are not imported\n" +
                  "             -s, --sfile, --source <sourcefile>\n"+
                  "                 File which has already been imported to GnuCash and occupies some IDs\n" +
                  "             -o, --ofile, --out, --output <outputfilename>\n"+
                  "                 File which will be created with new IDs\n")
            sys.exit()
        elif opt in ("-i", "--ifile", "--in", "--input"):
            inputfilename = arg
        elif opt in ("-s", "--sfile", "--source"):
            sourcefilename = arg
        elif opt in ("-o", "--ofile", "--out", "--output"):
            if arg.split(".")[1] & arg.split(".")[-1] == ".ofx":
                outputfilename = arg
            else:
                outputfilename = arg + ".ofx"
    print("Input file is: " + inputfilename)
    print("Original source file is: " + sourcefilename)
    print("Output file is: " + outputfilename)

    dedupeddom = deduplicate(inputfilename, sourcefilename)
    #dedupeddom.write('_inteligo_8859.ofx', pretty_print=True, encoding='iso-8859-2') # testing
    encoding, newdom = transform(dedupeddom)
    cleanup(newdom)
    newdom.write('_inteligo_8859.ofx', pretty_print=True, encoding='iso-8859-2')
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
