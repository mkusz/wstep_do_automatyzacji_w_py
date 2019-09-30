# Wstęp do automatyzacji w Python'ie

To repozytorium jest prezentacją wykonaną na potrzeby meetup'u Bielsko-BiałQA.

W repozytorium znajdują się 3 foldery:
 
 * **blog** - prosty blog w oparciu o Flask (uruchomienie poprzez plik *zayzafound.py*)
 * **presentation** - prezentacja w HTML'u (uruchomienie poprzez plik *index.html*)
 * **test** - testy
 
 Aby uruchomić przykładowy kod testów należy:
 
  1. Zainstalować przeglądarkę Chrome oraz odpowiedni dla konkretnej wersji przeglądarki Chrome WebDriver,
  2. Pobrać zawartość tego repozytorium do wybranego folderu
  3. W folderze utworzyć wirtualne środowisko Python'a (będąc w folderze wykonać polecenie `python3 -m venv ./venv`)
  4. Aktywować wirtualne środowisko (`./venv/bin/activate`)
  5. Zainstalować wymagane pakiety wykorzystwane przez blog oraz testy (`pip3 install -r requirements.txt`)
  6. Przejśc do folderu *blog*
  7. Uruchomić blog (`python3 ./zayzafoun.py`)
  
 Od tego momentu można uruchamiać testy z folderu *tests*.
 
 PS. Kod przygotowany i przetestowany w Python 3.6 oraz w środowisku Linux (powinien działać również na MacOSX oraz Linux). Powyższy kod powstał tylko i wyłącznie w celach prezentacyjnych i niekomercyjnych. Nie ponoszę jakiejkolwiek odpowiedzialności za jego działanie.