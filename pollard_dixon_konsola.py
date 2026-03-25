import time
import math
from random import randint
from math import log, exp, sqrt, gcd
import numpy as np
from typing import List, Optional

class PollardRho:
    def __init__(self, callback=None):
        self.callback = callback
        self.steps = []

    def factorize(self, n: int, seed: int = 2, max_iterations: int = 10000) -> Optional[int]:
        if n <= 1:
            return None

        if n % 2 == 0:
            if self.callback:
                self.callback("Liczba jest parzysta - dzielnik: 2\n")
            return 2

        self.steps = []
        x, y, d = seed, seed, 1
        iteration = 0

        def f(x):
            return (x * x + 1) % n

        if self.callback:
            self.callback(f"Rozpoczynanie algorytmu Rho Pollarda dla n = {n}\n")
            self.callback(f"Funkcja: f(x) = x² + 1 (mod {n})\n")
            self.callback(f"Wartość początkowa: x₀ = y₀ = {seed}\n\n")

        while d == 1 and iteration < max_iterations:
            x = f(x)
            y = f(f(y))
            d = gcd(abs(x - y), n)

            step_info = {'iteration': iteration + 1, 'x': x, 'y': y, 'diff': abs(x - y), 'gcd': d}
            self.steps.append(step_info)

            if self.callback and iteration < 50:  # Ograniczamy wyświetlanie kroków
                self.callback(f"Iteracja {iteration + 1:3d}: x = {x:8d}, y = {y:8d}, "
                              f"|x-y| = {abs(x - y):8d}, gcd = {d:8d}\n")

            iteration += 1
        
        if self.callback and iteration >= 50:
            self.callback("... (pominięto dalsze kroki w celu zachowania czytelności) ...\n")

        if d != n and d > 1:
            if self.callback:
                self.callback(f"\n✓ Znaleziono dzielnik: {d}\n")
                self.callback(f"✓ Sprawdzenie: {n} = {d} × {n // d}\n")
            return d
        elif iteration >= max_iterations:
            if self.callback:
                self.callback(f"\n⚠ Przekroczono maksymalną liczbę iteracji ({max_iterations})\n")
        else:
            if self.callback:
                self.callback(f"\n⚠ Algorytm nie znalazł dzielnika (d = n = {n})\n")

        return None


class Dixon:

    def __init__(self, callback=None):
        self.callback = callback

    def powmod(self, x: int, n: int, m: int) -> int:
        ans = 1
        x = x % m
        while n > 0:
            if n & 1:
                ans = (ans * x) % m
            x = (x * x) % m
            n >>= 1
        return ans

    def primes(self, n: int) -> List[int]:
        if n <= 0:
            return []
        if n <= 10:
            bound = 50
        else:
            bound = int(n * log(n) + n * log(log(n))) + 100
        sieve = [True] * (bound + 1)
        sieve[0] = sieve[1] = False
        for i in range(2, int(sqrt(bound)) + 1):
            if sieve[i]:
                for j in range(i * i, bound + 1, i):
                    sieve[j] = False
        primes_list = [i for i, is_p in enumerate(sieve) if is_p]
        return primes_list[:n]

    def factor_with_base(self, n: int, base: List[int]) -> Optional[List[int]]:
        factors = [0] * len(base)
        temp_n = n
        for i, p in enumerate(base):
            while temp_n % p == 0:
                temp_n //= p
                factors[i] += 1
        return factors if temp_n == 1 else None

    def gaussian_elimination_gf2(self, matrix: List[List[int]]) -> Optional[List[int]]:
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0
        augmented = [row[:] + [int(i == j) for j in range(rows)] for i, row in enumerate(matrix)]
        
        pivot_row = 0
        for col in range(cols):
            if pivot_row < rows:
                i = pivot_row
                while i < rows and augmented[i][col] == 0:
                    i += 1
                if i < rows:
                    augmented[pivot_row], augmented[i] = augmented[i], augmented[pivot_row]
                    for j in range(rows):
                        if j != pivot_row and augmented[j][col] == 1:
                            for k in range(len(augmented[j])):
                                augmented[j][k] ^= augmented[pivot_row][k]
                    pivot_row += 1

        for row in augmented:
            if all(val == 0 for val in row[:cols]):
                solution = [i for i, val in enumerate(row[cols:]) if val == 1]
                if solution:
                    return solution
        return None

    def factorize(self, n: int) -> Optional[int]:
        if n <= 1: return None
        if n % 2 == 0: return 2

        for k in range(2, int(log(n, 2)) + 1):
            root = round(n ** (1 / k))
            if root ** k == n:
                if self.callback: self.callback(f"Liczba {n} jest {k}-tą potęgą liczby {r}\n")
                return root

        if self.callback: self.callback(f"Rozpoczynanie algorytmu Dixona dla n = {n}\n")

        L = exp(sqrt(log(n) * log(log(n))))
        B_size = max(int(L**0.5), 10)
        B = self.primes(B_size)
        if self.callback:
            self.callback(f"Rozmiar bazy B: {B_size}\n")
            self.callback(f"Baza B: {B[:min(15, len(B))]}{'...' if len(B) > 15 else ''}\n\n")

        if self.callback: self.callback("Szukanie B-gładkich liczb...\n")
        smooth_numbers, x_values, factor_vectors = [], [], []
        max_attempts = B_size * 10

        while len(smooth_numbers) < B_size + 5 and len(x_values) < max_attempts:
            x = randint(int(sqrt(n)) + 1, n - 1)
            y = pow(x, 2, n)
            factors = self.factor_with_base(y, B)
            if factors:
                smooth_numbers.append(y)
                x_values.append(x)
                factor_vectors.append(factors)
                if self.callback and len(smooth_numbers) <= 8:
                    factor_str = ' × '.join([f"{B[i]}^{factors[i]}" for i in range(len(factors)) if factors[i] > 0])
                    self.callback(f"B-gładka: {x}² ≡ {y} ≡ {factor_str} (mod {n})\n")

        if len(smooth_numbers) < B_size + 1:
            if self.callback: self.callback("⚠ Nie udało się znaleźć wystarczającej liczby B-gładkich liczb\n")
            return None
        if self.callback: self.callback(f"\n✓ Znaleziono {len(smooth_numbers)} B-gładkich liczb\n\n")

        if self.callback: self.callback("Eliminacja Gaussa w GF(2)...\n")
        matrix = [[f % 2 for f in factors] for factors in factor_vectors]
        solution_indices = self.gaussian_elimination_gf2(matrix)

        if solution_indices is None:
            if self.callback: self.callback("⚠ Nie znaleziono rozwiązania w eliminacji Gaussa\n")
            return None
        if self.callback: self.callback(f"✓ Znaleziono rozwiązanie: kombinacja wierszy {solution_indices}\n")

        a = 1
        for idx in solution_indices: a = (a * x_values[idx]) % n
        
        combined_factors = [sum(factor_vectors[idx][i] for idx in solution_indices) for i in range(len(B))]
        b = 1
        for i in range(len(B)): b = (b * self.powmod(B[i], combined_factors[i] // 2, n)) % n

        if self.callback:
            self.callback(f"a = {a}\n")
            self.callback(f"b = {b}\n")

        if a == b or a == n - b:
            if self.callback: self.callback("⚠ Niefortunny przypadek: a ≡ ±b (mod n). Spróbuj ponownie.\n")
            return None

        factor = gcd(abs(a - b), n)
        if 1 < factor < n:
            if self.callback:
                self.callback(f"\n✓ Znaleziono dzielnik: {factor}\n")
                self.callback(f"✓ Sprawdzenie: {n} = {factor} × {n // factor}\n")
            return factor
        return None


def run_pollard_rho(n, verbose):
    print(f"\n{'=' * 25}\n WYNIKI RHO POLLARDA \n{'=' * 25}")
    callback = print if verbose else None
    pollard = PollardRho(callback=callback)

    start_time = time.time()
    factor = pollard.factorize(n)
    end_time = time.time()

    if factor:
        print(f"\n✅ Sukces! Znaleziony dzielnik: {factor}")
        print(f"📊 Sprawdzenie: {n} = {factor} × {n // factor}")
    else:
        print(f"\n❌ Nie znaleziono dzielnika.")

    print(f"⏱️  Czas wykonania: {end_time - start_time:.6f} s")
    print(f"🔄 Liczba iteracji: {len(pollard.steps)}")

def run_dixon(n, verbose):
    print(f"\n{'=' * 25}\n WYNIKI ALGORYTMU DIXONA \n{'=' * 25}")
    callback = print if verbose else None
    dixon = Dixon(callback=callback)

    start_time = time.time()
    factor = dixon.factorize(n)
    end_time = time.time()

    if factor:
        print(f"\n✅ Sukces! Znaleziony dzielnik: {factor}")
        print(f"📊 Sprawdzenie: {n} = {factor} × {n // factor}")
    else:
        print(f"\n❌ Nie znaleziono dzielnika.")

    print(f"⏱️  Czas wykonania: {end_time - start_time:.6f} s")

def run_comparison(n, show_steps):
    print(f"\n{'=' * 40}\n PORÓWNANIE ALGORYTMÓW DLA LICZBY {n} \n{'=' * 40}")
    runs = 3
    results = {'pollard_rho': {'times': [], 'factors': [], 'steps': []},
               'dixon': {'times': [], 'factors': []}}
    callback = print if show_steps else None

    # Test Pollard Rho
    print("\n--- 🔵 Testowanie Rho Pollarda ---")
    for i in range(runs):
        print(f"\nPrzebieg {i + 1}/{runs}:")
        pollard = PollardRho(callback=callback)
        start_time = time.time()
        factor = pollard.factorize(n)
        end_time = time.time()
        results['pollard_rho']['times'].append(end_time - start_time)
        results['pollard_rho']['factors'].append(factor)
        results['pollard_rho']['steps'].append(len(pollard.steps))
        print(f"Wynik: {'Dzielnik ' + str(factor) if factor else 'Brak'}")
        print(f"Czas: {end_time - start_time:.6f}s, Kroki: {len(pollard.steps)}")

    # Test Dixon
    print("\n--- 🔴 Testowanie Dixona ---")
    for i in range(runs):
        print(f"\nPrzebieg {i + 1}/{runs}:")
        dixon = Dixon(callback=callback)
        start_time = time.time()
        factor = dixon.factorize(n)
        end_time = time.time()
        results['dixon']['times'].append(end_time - start_time)
        results['dixon']['factors'].append(factor)
        print(f"Wynik: {'Dzielnik ' + str(factor) if factor else 'Brak'}")
        print(f"Czas: {end_time - start_time:.6f}s")
    
    # Podsumowanie
    print(f"\n\n{'=' * 20}\n PODSUMOWANIE \n{'=' * 20}")
    for algo_name, data in results.items():
        algo_display = "🔵 Rho Pollarda" if algo_name == "pollard_rho" else "🔴 Dixon"
        successful_runs = sum(1 for f in data['factors'] if f is not None)
        print(f"\n{algo_display}:")
        print(f"  📊 Skuteczność: {successful_runs}/{runs} ({successful_runs / runs * 100:.1f}%)")
        if data['times']:
             print(f"  ⏱️  Średni czas: {np.mean(data['times']):.6f} s")
             print(f"  ⚡ Min/Max czas: {min(data['times']):.6f}s / {max(data['times']):.6f}s")
        if algo_name == "pollard_rho" and data['steps']:
            print(f"  🔄 Średnia liczba kroków: {np.mean(data['steps']):.1f}")
        if successful_runs > 0:
            found_factors = {f for f in data['factors'] if f is not None}
            print(f"  🎯 Znalezione dzielniki: {found_factors}")

# --- Główna pętla programu ---

def uruchom_konsole():
    print("--- ALGORYTMY FAKTORYZACJI: RHO POLLARDA & DIXON ---")
    
    while True:
        print("\n" + "="*50)
        print("Wybierz opcję:")
        print("  1. Uruchom algorytm Rho Pollarda")
        print("  2. Uruchom algorytm Dixona")
        print("  3. Porównaj oba algorytmy")
        print("  4. Wyjdź z programu")
        
        choice = input("Twój wybór [1-4]: ")

        if choice == '4':
            print("Do widzenia!")
            break

        if choice not in ['1', '2', '3']:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")
            continue

        try:
            number_str = input("Podaj liczbę całkowitą do faktoryzacji: ")
            n = int(number_str)
            if n <= 1:
                print("Błąd: Liczba musi być większa od 1.")
                continue
        except ValueError:
            print("Błąd: Podano nieprawidłową wartość. Wprowadź liczbę całkowitą.")
            continue

        verbose_choice = input("Czy chcesz wyświetlać szczegółowe kroki? [t/n]: ").lower()
        verbose = verbose_choice == 't'

        if choice == '1':
            run_pollard_rho(n, verbose)
        elif choice == '2':
            run_dixon(n, verbose)
        elif choice == '3':
            run_comparison(n, verbose)

if __name__ == "__main__":
    uruchom_konsole()