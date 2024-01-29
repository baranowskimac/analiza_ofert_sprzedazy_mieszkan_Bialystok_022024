# OtodomDataScraper

Repozytorium do scrapowania ofert sprzedaży i wynajmu domów i mieszkań z serwisu OtoDom.  
Kod przygotowany na zaliczenie studiów podyplomowych.

## Jak korzystać

1. Instalacja potrzebnych bibliotek:

    ```bash
    pip install -r requirements.txt
    ```

2. Wykonanie zapytania:
    - Uzupełnij warunki zapytania w pliku konfiguracyjnym:

    ```python
    ./config/query_params.yaml
    ```

    - uruchom skrypt

    ```bash
    python main.py
    ```

3. Wyniki
    - batchowe dane odkładają się w folderze `./batch/`
    - pełny df zapisuje się w folderze `./full_df`

## Argumenty reklam w configu

1. Podstawowe argumenty:
    - main_page: <https://www.otodom.pl/pl/wyniki/>  
        główna strona serwisu Oto Dom. **Nie zmieniać**
    - offer_type:  
        Typ ofery. Możliwe argumenty: sprzedaz / wynajem
    - apartament_type:  
        typ szukanego lokum  
        możliwe wartości: mieszkanie/kawalerka/dom/inwestycja/pokoj/dzialka/lokal/haleimagazyny/garaz  
2. Argumenty dla lokalizacji szukanych ofert:  
    1. Uwagi
        - Jeżeli region i city pozostaną puste - program wyszuka oferty dla całej Polski
        - Jeżeli poszukiwane są oferty dla miasta - region (województwo) w którym dane miasto się znajduje również musi być wypełnione
            (jeżeli nie zostanie wypełnione wynikiem działania programu będzie Error 404)
        - nazwy województw/miast wpisujemy bez polskich znaków  
    2. Argumenty
        - region:
            Województwo polskie. Możliwe wartości:
            dolnoslaskie/kujawsko--pomorskie/lodzkie/lubelskie/lubuskie/malopolskie/mazowieckie/opolskie/podkarpackie/
            podlaskie/pomorskie/slaskie/swietokrzyskie/warminsko--mazurskie
        - city:
            Nazwa miasta do przeszukiwania ofert. najniższy poziom miast do poszukiwań to miasta na prawach powiatu
        - distance_radius:
            promień (w km) wogół miasta w którym poszukiwane będą również oferty.
            UWAGA: działą tylko w sytuacji gdy zostanie podane miasto. W innym przypadku argument powinien zostać pusty
3. Argumenty ceny
    - price_min/price_max - cena minimalna ofert/cena maxymalna poszukiwanych ofert. W złotych polskich.
    - W przypadku price_min pozostawienie pola pustego - oferty będą przeszukiwane od 0 zł
    - W przypadku price_max pozostawienie pola pustego - brak górnego pułapu cenowego przeszukiwanych ofert
4. Ustawienia systemowe
    - limit:  
        limit liczby reklam na jednej stronie. Możliwe wartości: 24/36/48/72
    - sys_sleep:  
        uśpienie działania programu pomiędzy kolejnymi odpytywaniami serwisu. Ustawiane w celu uniknięcia zablokowania.
        Wartości podwana w sekundach.
