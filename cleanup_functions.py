#!/bin/python3
# Copyright 2022 Łukasz Herok, HighPriest@Hiero Software
# Contact person: HighPriest@github

import re

#region HELPER_FUNCTIONS
def _przelew_extract(memo):
    m = re.match(r".*(?P<nr_rach>(?<=Nr rach. przeciwst.: )(?:.*))?Dane adr\. rach\. przeciwst\.: (?P<adres>(?<=Dane adr\. rach\. przeciwst\.: )(?:.*)) Tytuł: (?P<tytul>(?<=Tytuł: )(?:.*)) Data waluty: (?P<data_waluty>(?<=Data waluty: )(?:.*))", memo.text)
    konto = m.group('nr_rach')
    kto = m.group('adres')
    co = m.group('tytul')
    return konto, kto, co

def _karta_extract(memo):
    m = re.match(r".*(?P<tytul>(?<=Tytuł: )(?:.*))?Lokalizacja: Kraj: (?P<kraj>(?<=Kraj: )(?:.*)) Miasto: (?P<miasto>(?<=Miasto: )(?:.*)) Adres: (?P<adres>(?<=Adres: )(?:.*)) Data wykonania: (?P<data_zgloszenia>(?<=Data wykonania: )(?:.*)) Numer referencyjny: (?P<nr_ref>(?<=Numer referencyjny: )(?:.*)) Oryginalna kwota operacji: (?P<kwota>(?<=Oryginalna kwota operacji: )(?:.*))\s(?P<waluta>(?:\w{3})) Numer karty: \* (?P<nr_karty>(?<=Numer karty: \* )(?:.{4})) Data waluty: (?P<data_realizacji>(?<=Data waluty: )(?:.*))", memo.text)
    tytul = m.group('tytul')
    kraj = m.group('kraj')
    miasto = m.group('miasto')
    adres = m.group('adres')
    data_zgloszenia = m.group('data_zgloszenia')
    numer_ref = m.group('nr_ref')
    kwota = m.group('kwota')
    waluta = m.group('waluta')
    karta = m.group('nr_karty')
    data_realizacji = m.group('data_realizacji')
    return adres + " " + miasto, karta, kwota, waluta

def _wyplata_extract(memo):
    m = re.match(r".*(?P<tytul>(?<=Tytuł: )(?:.*))?Lokalizacja: Kraj: (?P<kraj>(?<=Kraj: )(?:.*)) Miasto: (?P<miasto>(?<=Miasto: )(?:.*)) Adres: (?P<adres>(?<=Adres: )(?:.*)) Data wykonania: (?P<data_zgloszenia>(?<=Data wykonania: )(?:.*)) Numer referencyjny: (?P<nr_ref>(?<=Numer referencyjny: )(?:\S*)).* Bankomat: (?P<bankomat>(?<=Bankomat: )(?:.*)) Numer telefonu: (?P<nr_telefonu>(?<=Numer telefonu: )(?:.*))  Data waluty: (?P<data_realizacji>(?<=Data waluty: )(?:.*))", memo.text)
    tytul = m.group('tytul')
    kraj = m.group('kraj')
    miasto = m.group('miasto')
    adres = m.group('adres')
    data_zgloszenia = m.group('data_zgloszenia')
    numer_ref = m.group('nr_ref')
    bankomat = m.group('bankomat')
    nr_tel = m.group('nr_telefonu')
    data_realizacji = m.group('data_realizacji')
    return adres + " " + miasto, bankomat

def _platnosc_web_extract(memo):
    #TODO: fix this regexp
    #(?P<tytul>(?<=Tytuł: )(?:.*))?Lokalizacja:(?:\s+Kraj:\s(?P<kraj>(?:.*?)))?(?:\s+Miasto:\s(?P<miasto>(?:.*?)))? Adres: (?P<adres>(?<=Adres: )(?:.*)) Data wykonania: (?P<data_zgloszenia>(?<=Data wykonania: )(?:.*)) Numer referencyjny: (?P<nr_ref>(?<=Numer referencyjny: )(?:\S*)).* Numer telefonu: (?P<nr_telefonu>(?<=Numer telefonu: )(?:.*))  Data waluty: (?P<data_realizacji>(?<=Data waluty: )(?:.*))
    m = re.match(r"(?:.*Tytuł:\s(?P<tytul>(?:.*?)) )?Lokalizacja:(?:\s+Kraj:\s(?P<kraj>(?:.*?)))?(?:\s+Miasto:\s(?P<miasto>(?:.*?)))?(?:\s+Adres:\s(?P<adres>(?:.*?)) )?(?:Data wykonania:\s(?P<data_zgloszenia>(?:.*?)))?(?:\s+Kwota CashBack:\s(?P<cashback>(?:.*?)))?(?:\s+Numer referencyjny:\s(?P<nr_ref>(?:.*?)))?(?:\s+Oryginalna kwota operacji:\s(?P<kwota>(?:.*?)))?(?:\s+Numer karty:\s\*\s(?P<nr_karty>(?:.*?)))?(?:\s+Numer telefonu:\s(?P<nr_tel>(?:.*)))?\s+Data waluty: (?P<data_realizacji>(?:.*))", memo.text)
    if m == None:
        m = re.match(r".*(?P<nr_rach>(?<=Nr rach. przeciwst.: )(?:.*))?Dane adr\. rach\. przeciwst\.: (?P<adres>(?<=Dane adr\. rach\. przeciwst\.: )(?:.*)) Tytuł: (?P<tytul>(?<=Tytuł: )(?:.*)) Data waluty: (?P<data_realizacji>(?<=Data waluty: )(?:.*))", memo.text)
    if re.search(r"Tytuł:", memo.text) is not None:
        tytul = m.group('tytul')
    else:
        tytul = ''
    if re.search(r"Adres:", memo.text) is not None:
        adres = m.group('adres')
    else:
        adres = ''
    if re.search(r"Kraj:", memo.text) is not None:
        kraj = m.group('kraj')
    else:
        kraj = ''
    if re.search(r"Miasto:", memo.text) is not None:
        miasto = m.group('miasto')
    else:
        miasto = ''
    if re.search(r"Data wykonania:", memo.text) is not None:
        data_zgloszenia = m.group('data_zgloszenia')
    else:
        data_zgloszenia = ''
    if re.search(r"Numer referencyjny:", memo.text) is not None:
        numer_ref = m.group('nr_ref')
    else:
        numer_ref = ''
    if re.search(r"Numer telefonu:", memo.text) is not None:
        nr_tel = m.group('nr_tel')
    else:
        nr_tel = ''
    if re.search(r"Data waluty:", memo.text) is not None:
        data_realizacji = m.group('data_realizacji')
    else:
        data_realizacji = ''
    return tytul, adres + " " + miasto

def _oplata_extract(memo):
    m = re.match(r"(?:.*Tytuł:\s(?P<tytul>(?:.*?)))?(?:\,)? (?:(?P<okres>(?:\d?\d\.\d\d\-\d?\d\.\d\d)))?\s?Data waluty: (?P<data_realizacji>(?<=Data waluty: )(?:.*))", memo.text)
    if re.search(r"Tytuł:", memo.text) is not None:
        tytul = m.group('tytul')
    else:
        tytul = ''
    if re.search(r"(\d?\d\.\d\d\-\d?\d\.\d\d)", memo.text) is not None:
        okres = m.group('okres')
    else:
        okres = ''
    data_realizacji = m.group('data_realizacji')
    return tytul, okres

def _cleanup_desc(name, extname, memo):
    if 'Przelew z rachunku' in name.text or 'Zlecenie stałe' in name.text:
        konto, kto, co = _przelew_extract(memo)
        extname.text = co + ', dla: ' + kto
        memo.text = co + ', dla: ' + kto
        name.text = name.text + ', dla: ' + kto
    elif 'Przelew' in name.text:
        konto, kto, co = _przelew_extract(memo)
        if konto is not None:
            extname.text = co + ', od: ' + kto + '; Nr Konta: ' + konto
        else:
            extname.text = co + ', od: ' + kto
        memo.text = co + ', od: ' + kto
        name.text = name.text + ', od: ' + kto
    elif 'Płatność kartą' in name.text or 'Wypłata z bankomatu' in name.text:
        adres, karta, kwota, waluta = _karta_extract(memo)
        if(waluta != 'PLN' ):
            extname.text = 'Karta: ' + karta + ', w: ' + adres + '; Kwota: ' + kwota + ' ' + waluta
            memo.text = 'Karta: ' + karta + ', w: ' + adres
            name.text = name.text + ', w: ' + adres
        elif(waluta == 'PLN'):
            extname.text = 'Karta: ' + karta + ', w: ' + adres
            memo.text = "Karta: " + karta + ', w: ' + adres
            name.text = name.text + ", w: " + adres
    elif 'Wypłata w bankomacie' in name.text:
        adres, bankomat = _wyplata_extract(memo)
        extname.text = bankomat + ", w " + adres
        memo.text = name.text + ", " + bankomat + ", w " + adres
        name.text = name.text + ", w: " + adres
    elif 'Płatność web' in name.text or 'Zwrot' in name.text:
        tytul, adres = _platnosc_web_extract(memo)
        if (tytul):
            extname.text = ''
            memo.text = tytul + ', ' + adres
            name.text = name.text + ', ' + adres
        else:
            extname.text = ''
            memo.text = name.text + ', ' + adres
            name.text = name.text + ', ' + adres

    elif 'Opłata' in name.text or 'Prowizja' in name.text:
        tytul, okres = _oplata_extract(memo)
        if okres != '':
            extname.text = tytul + ', okres: ' + okres
            memo.text = name.text + " " + tytul + ', okres: ' + okres
            name.text = name.text
        else:
            extname.text = tytul
            memo.text = name.text + " " + tytul
            name.text = name.text
#endregion HELPER_FUNCTIONS

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
