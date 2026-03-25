# Factorization Lab: Pollard's Rho vs Dixon's Algorithm

Interaktywna aplikacja w Pythonie służąca do faktoryzacji liczb całkowitych, pozwalająca na porównanie wydajności i mechaniki dwóch słynnych algorytmów teorii liczb.

## 🚀 O projekcie
Projekt powstał jako narzędzie edukacyjne do demonstracji różnic między probabilistycznym podejściem algorytmu Rho Pollarda a bardziej zaawansowaną metodą losowych kwadratów Dixona. [cite_start]Program posiada responsywny interfejs GUI, dzięki czemu obliczenia nie blokują działania aplikacji[cite: 57, 65].

### Główne funkcjonalności:
* [cite_start]**Faktoryzacja dowolnych liczb:** Wprowadź liczbę i sprawdź jej dzielniki[cite: 61].
* [cite_start]**Tryb porównawczy:** Uruchom oba algorytmy jednocześnie, aby zobaczyć różnice w czasie i liczbie kroków[cite: 62].
* [cite_start]**Szczegółowy podgląd:** Kontroluj poziom szczegółowości logów wyświetlanych w trakcie obliczeń[cite: 63, 64].
* [cite_start]**Wizualizacja matematyki:** Śledź postępy algorytmów w dedykowanym polu tekstowym[cite: 64].

## 🧠 Zastosowane Algorytmy

### 1. Algorytm Rho Pollarda
[cite_start]Metoda oparta na "paradoksie dnia urodzin" i wykrywaniu cykli Floyda ("żółw i zając"). [cite_start]Jest niezwykle efektywna w znajdowaniu mniejszych dzielników[cite: 69].
* [cite_start]**Funkcja generująca:** $f(x) = (x^2 + 1) \pmod{n}$[cite: 80].
* [cite_start]**Mechanizm:** Wykorzystuje NWD do znalezienia kolizji modulo dzielnik $p$[cite: 77, 87].

### 2. Algorytm Dixona
"Ciężka artyleria" faktoryzacji. [cite_start]Wykorzystuje bazy liczb pierwszych i eliminację Gaussa do znajdowania kongruencji kwadratów[cite: 29]. Idealny do liczb, przy których prostsze metody zawodzą.

## 🛠️ Technologie
* **Język:** Python
* **Interfejs:** Biblioteka GUI (np. Tkinter/PyQt – *wpisz odpowiednią*)
* [cite_start]**Algorytmika:** Wielowątkowość (threading) dla płynności działania[cite: 65].

## 📖 Jak uruchomić
1. Sklonuj repozytorium: `git clone https://github.com/TWOJA-NAZWA/Rho-vs-Dixon.git`
2. Wejdź do folderu: `cd Rho-vs-Dixon`
3. Uruchom program: `python main.py`

## 👤 Autor
[cite_start]**Norbert Wójcik** [cite: 53]
