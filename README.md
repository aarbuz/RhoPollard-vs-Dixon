# Factorization Lab: Pollard's Rho & Dixon's Algorithm

Interaktywna aplikacja w Pythonie służąca do faktoryzacji liczb całkowitych. Projekt pozwala na porównanie dwóch klasycznych podejść algorytmicznych: probabilistycznej metody **Rho Pollarda** oraz metody **losowych kwadratów Dixona**.

## 🎯 Cel projektu
Program powstał jako narzędzie edukacyjne do demonstracji różnic w wydajności i mechanice działania algorytmów teorii liczb. Pozwala zrozumieć, dlaczego niektóre liczby są "łatwiejsze" do złamania od innych.

## ✨ Funkcje aplikacji
* **GUI (Tkinter/CustomTkinter):** Intuicyjny interfejs, który nie blokuje się podczas obliczeń dzięki zastosowaniu wielowątkowości (`threading`).
* **Tryb porównawczy:** Możliwość uruchomienia obu algorytmów jednocześnie dla tej samej liczby.
* **Logowanie kroków:** Szczegółowy podgląd procesów zachodzących "pod maską" (np. znajdowanie relacji w algorytmie Dixona).
* **Obsługa dużych liczb:** Wykorzystanie natywnej precyzji Pythona do operacji na dużych liczbach całkowitych.

## 🧠 Opis algorytmów

### 1. Algorytm Rho Pollarda
"Zwinny zwiadowca" – szybki i lekki, oparty na paradoksie dnia urodzin i wykrywaniu cykli Floyda.
* **Zastosowanie:** Idealny do znajdowania mniejszych dzielników.
* **Mechanizm:** Wykorzystuje funkcję $f(x) = (x^2 + 1) \pmod{n}$ do generowania sekwencji, w której szukamy kolizji modulo dzielnik $p$.

### 2. Algorytm Dixona
"Ciężka artyleria" – bardziej złożony algorytm, będący prekursorem sita kwadratowego.
* **Zastosowanie:** Skuteczny tam, gdzie prostsze metody zawiodą.
* **Mechanizm:** Buduje bazę liczb pierwszych, poszukuje relacji (gładkich liczb), a następnie wykorzystuje **eliminację Gaussa** na macierzy wykładników modulo 2, aby znaleźć kongruencję kwadratów.

## 🛠️ Instalacja i uruchomienie
1. Sklonuj repozytorium:
   ```bash
   git clone [https://github.com/TWOJA-NAZWA/nazwa-projektu.git](https://github.com/TWOJA-NAZWA/nazwa-projektu.git)
