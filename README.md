# gnucash-inteligo
Skrypt Python, pozwalający na zaimportowanie wyciągów z `Inteligo` do `Gnucash`.

## Użycie
1. Należy pobrać wyciąg z Inteligo w formacie xml i zapisać go jako historia.xml.
   1. Pliki dostępne są poprzez wybranie opcji "Pobierz historię" a następnie "w formacie xml" na stronie historii rachunku.
2. `python transform.py -i historia.xml -o inteligo.ofx`
3. Wygenerowany zostanie plik w formacie **.ofx**, który można zaimportować do GnuCash.

## Uwaga FAQ
1. WINDOWSOWY IMPORTER PLIKÓW .OFX JEST USZKODZONY.
Jest to niezależne od tego skryptu, który generuje poprawnie zakodowane pliki, które w importerze GnuCash uruchomionym na Windowsie, zostaną odczytane błędnie. Aby transakcje poprawnie zapisały się w portfelu GnuCash, import należy przeprowadzić pod systemem Linux.
2. TODO: Inteligo również udostępnia podsumowania w postaci comiesięcznych wiadomości mailowych.  
Pliki te, pomimo zgodnej nazwy, posiadają trochę inną strukturę. Aby móc je konwertować do formatu zgodnego z gnucash, potrzebna jest modyfikacja template'u XSL.
3. W repozytorium dostępny jest alternatywny skrypt, dla transakcji sprzed 2014 roku. Powinien on pozwolić wam zaimportować transakcje z podobnym rezultatem, co w wypadku nowszych opisów. 
4. Jeżeli po zaimportowaniu dwóch różnych zbiorów transakcji (e.g. pre2014 i post2014, lub post2014 i nowszy miesiąc) i zauważycie iż nie zgadza się wam końcowe saldo, są duże szanse że niezaimportowały się transakcje o takich samych identyfikatorach. Jest to błąd ze strony inteligo.
Żeby naprawić ten błąd ręcznie, należy skorzystać ze skryptu `deduplicate.py`, podać plik z brakującymi transakcjami jako 'inputfile' (e.g. *historia.xml*), a poprawnie zaimportowany wcześniej plik, podać jako 'sourcefile' (e.g. *historia_old.xml*). Otrzymamy plik inteligo.ofx z brakującymi transakcjami do zaimportowania.
Ten błąd jest poprawiany automatycznie w najnowszych skryptach tego projektu. Każdy przepuszczony w przyszłości plik .xml przez `transform.py`, nie będzie miał problemu z nachodzącymi na siebie identyfikatorami.

## Notes
- Dobre narzędzie do sprawdzania pythonowych regex'ów: https://regex101.com/
- **GNU GENERAL PUBLIC LICENSE**
