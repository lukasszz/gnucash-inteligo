# gnucash-inteligo
Skrypt Python, pozwalający na zaimportowanie wyciągów z `Inteligo` do `Gnucash`.

## Użycie
1. Należy pobrać wyciąg z Inteligo w formacie xml i zapisać go jako historia.xml.
   1. Pliki dostępne są poprzez wybranie opcji "Pobierz historię" a następnie "w formacie xml" na stronie historii rachunku.
2. `python transform.py -i historia.xml -o inteligo.ofx`
3. Wygenerowany zostanie plik w formacie **.ofx**, który można zaimportować do GnuCash.

## Uwaga
1. Inteligo również udostępnia podsumowania w postaci comiesięcznych wiadomości mailowych.  
Pliki te, pomimo zgodnej nazwy, posiadają trochę inną strukturę. Aby móc je konwertować do formatu zgodnego z gnucash, potrzebna jest modyfikacja template'u XSL.
2. W repozytorium dostępny jest alternatywny skrypt, dla transakcji sprzed 2014 roku. Powinien on pozwolić wam zaimportować transakcje z podobnym rezultatem, co w wypadku nowszych opisów. 

## Notes
- Dobre narzędzie do sprawdzania pythonowych regex'ów: https://regex101.com/
- **GNU GENERAL PUBLIC LICENSE**