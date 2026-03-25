# Factorization Lab: Pollard's Rho vs Dixon's Algorithm

Interaktywna aplikacja w Pythonie służąca do faktoryzacji liczb całkowitych, pozwalająca na porównanie wydajności i mechaniki dwóch słynnych algorytmów teorii liczb.

## 🚀 O projekcie
Projekt powstał jako narzędzie edukacyjne do demonstracji różnic między probabilistycznym podejściem algorytmu Rho Pollarda a bardziej zaawansowaną metodą losowych kwadratów Dixona. Program posiada responsywny interfejs GUI, dzięki czemu obliczenia nie blokują działania aplikacji.

### Główne funkcjonalności:
* **Faktoryzacja dowolnych liczb:** Wprowadź liczbę i sprawdź jej dzielniki.
* **Tryb porównawczy:** Uruchom oba algorytmy jednocześnie, aby zobaczyć różnice w czasie i liczbie kroków.
* **Szczegółowy podgląd:** Kontroluj poziom szczegółowości logów wyświetlanych w trakcie obliczeń.
* **Wizualizacja matematyki:** Śledź postępy algorytmów w dedykowanym polu tekstowym.

## 🧠 Zastosowane Algorytmy

### 1. Algorytm Rho Pollarda
Metoda oparta na "paradoksie dnia urodzin" i wykrywaniu cykli Floyda ("żółw i zając"). Jest niezwykle efektywna w znajdowaniu mniejszych dzielników.
* **Funkcja generująca:** f(x) = (x^2 + 1) mod n.
* **Mechanizm:** Wykorzystuje NWD do znalezienia kolizji modulo dzielnik p.

### 2. Algorytm Dixona
"Ciężka artyleria" faktoryzacji. Wykorzystuje bazy liczb pierwszych i eliminację Gaussa do znajdowania kongruencji kwadratów. Idealny do liczb, przy których prostsze metody zawodzą.

## 🛠️ Technologie
* **Język:** Python
* **Interfejs:** Biblioteka GUI (np. Tkinter/PyQt – wpisz odpowiednią)
* **Algorytmika:** Wielowątkowość (threading) dla płynności działania.

## 📖 Jak uruchomić
1. Sklonuj repozytorium: `git clone https://github.com/TWOJA-NAZWA/Rho-vs-Dixon.git`
2. Wejdź do folderu: `cd Rho-vs-Dixon`
3. Uruchom program: `python main.py`

## 👤 Autor
**Norbert Wójcik**
