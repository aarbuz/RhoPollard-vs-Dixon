
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import math
from random import randint
from math import log, exp, sqrt, gcd
import numpy as np
from typing import List, Tuple, Optional, Dict, Any


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

            step_info = {
                'iteration': iteration + 1,
                'x': x,
                'y': y,
                'diff': abs(x - y),
                'gcd': d
            }
            self.steps.append(step_info)

            if self.callback and iteration < 50:  # Ograniczamy wyświetlanie dla GUI
                self.callback(f"Iteracja {iteration + 1:3d}: x = {x:8d}, y = {y:8d}, "
                              f"|x-y| = {abs(x - y):8d}, gcd = {d:8d}\n")

            iteration += 1

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
        self.steps = {}

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

        primes_list = []
        for i in range(2, bound + 1):
            if len(primes_list) >= n:
                break
            if sieve[i]:
                primes_list.append(i)

        return primes_list[:n]

    def factor_with_base(self, n: int, base: List[int]) -> Optional[List[int]]:
        factors = [0] * len(base)
        temp_n = n

        for i, p in enumerate(base):
            while temp_n % p == 0:
                temp_n //= p
                factors[i] += 1

        if temp_n == 1:
            return factors
        return None

    def gaussian_elimination_gf2(self, matrix: List[List[int]]) -> Optional[List[int]]:
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0

        augmented = []
        for i in range(rows):
            row = matrix[i][:] + [0] * rows
            row[cols + i] = 1
            augmented.append(row)

        pivot_row = 0
        for col in range(cols):
            found_pivot = False
            for row in range(pivot_row, rows):
                if augmented[row][col] == 1:
                    augmented[pivot_row], augmented[row] = augmented[row], augmented[pivot_row]
                    found_pivot = True
                    break

            if not found_pivot:
                continue

            for row in range(rows):
                if row != pivot_row and augmented[row][col] == 1:
                    for c in range(cols + rows):
                        augmented[row][c] ^= augmented[pivot_row][c]

            pivot_row += 1

        for row in range(rows):
            is_zero_row = all(augmented[row][c] == 0 for c in range(cols))
            if is_zero_row:
                solution = []
                for c in range(cols, cols + rows):
                    if augmented[row][c] == 1:
                        solution.append(c - cols)
                return solution

        return None

    def factorize(self, n: int) -> Optional[int]:
        if n <= 1:
            return None

        if n % 2 == 0:
            return 2

        # Sprawdź czy n jest potęgą
        for k in range(2, int(log(n, 2)) + 1):
            root = int(n ** (1 / k))
            for r in [root - 1, root, root + 1]:
                if r ** k == n:
                    if self.callback:
                        self.callback(f"Liczba {n} jest {k}-tą potęgą liczby {r}\n")
                    return r

        if self.callback:
            self.callback(f"Rozpoczynanie algorytmu Dixona dla n = {n}\n")

        # Faza 1: Wybór bazy faktorów
        L = exp(sqrt(log(n) * log(log(n))))
        B_size = max(int(sqrt(L)), 10)
        B = self.primes(B_size)

        if self.callback:
            self.callback(f"Rozmiar bazy B: {B_size}\n")
            self.callback(f"Baza B: {B[:min(15, len(B))]}{'...' if len(B) > 15 else ''}\n\n")

        # Faza 2: Znajdowanie B-gładkich liczb
        smooth_numbers = []
        x_values = []
        factor_vectors = []

        max_attempts = B_size * 8
        attempts = 0

        if self.callback:
            self.callback("Szukanie B-gładkich liczb...\n")

        while len(smooth_numbers) < B_size + 3 and attempts < max_attempts:
            x = randint(2, n - 1)
            if gcd(x, n) > 1:
                factor = gcd(x, n)
                if self.callback:
                    self.callback(f"✓ Znaleziono dzielnik podczas wyboru x: {factor}\n")
                return factor

            y = (x * x) % n
            factors = self.factor_with_base(y, B)

            if factors is not None:
                smooth_numbers.append(y)
                x_values.append(x)
                factor_vectors.append(factors)

                if self.callback and len(smooth_numbers) <= 8:
                    factor_str = ' × '.join([f"{B[i]}^{factors[i]}" for i in range(len(factors)) if factors[i] > 0])
                    self.callback(f"B-gładka: {x}² ≡ {y} ≡ {factor_str} (mod {n})\n")

            attempts += 1

        if len(smooth_numbers) < B_size + 1:
            if self.callback:
                self.callback("⚠ Nie udało się znaleźć wystarczającej liczby B-gładkich liczb\n")
            return None

        if self.callback:
            self.callback(f"✓ Znaleziono {len(smooth_numbers)} B-gładkich liczb\n\n")

        # Faza 3: Eliminacja Gaussa w GF(2)
        if self.callback:
            self.callback("Eliminacja Gaussa w GF(2)...\n")

        matrix = [[factors[i] % 2 for i in range(len(B))] for factors in factor_vectors]
        solution_indices = self.gaussian_elimination_gf2(matrix)

        if solution_indices is None:
            if self.callback:
                self.callback("⚠ Nie znaleziono rozwiązania w eliminacji Gaussa\n")
            return None

        if self.callback:
            self.callback(f"✓ Znaleziono rozwiązanie: kombinacja wierszy {solution_indices}\n")

        # Oblicz a i b
        a = 1
        combined_factors = [0] * len(B)

        for idx in solution_indices:
            a = (a * x_values[idx]) % n
            for i in range(len(B)):
                combined_factors[i] += factor_vectors[idx][i]

        b = 1
        for i in range(len(B)):
            if combined_factors[i] > 0:
                b = (b * pow(B[i], combined_factors[i] // 2)) % n

        if self.callback:
            self.callback(f"a = {a}\n")
            self.callback(f"b = {b}\n")

        # Sprawdź czy a ≢ ±b (mod n)
        if a % n == b % n or a % n == (-b) % n:
            if self.callback:
                self.callback("⚠ Niefortunny przypadek: a ≡ ±b (mod n)\n")
            return None

        factor1 = gcd(a - b, n)
        factor2 = gcd(a + b, n)

        result = None
        if 1 < factor1 < n:
            result = factor1
        elif 1 < factor2 < n:
            result = factor2

        if self.callback and result:
            self.callback(f"\n✓ Znaleziono dzielnik: {result}\n")
            self.callback(f"✓ Sprawdzenie: {n} = {result} × {n // result}\n")

        return result

#gui
class FactorizationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorytmy Faktoryzacji - Rho Pollarda & Dixon")
        self.root.geometry("900x700")
        self.root.configure(bg='#222222')

        # Zmienne
        self.number_var = tk.StringVar()
        self.algorithm_var = tk.StringVar(value="pollard")
        self.verbose_var = tk.BooleanVar(value=True)
        self.compare_steps_var = tk.BooleanVar(value=True)

        self.create_widgets()

    def create_widgets(self):
        # Nagłówek
        header_frame = tk.Frame(self.root, bg='#333333', height=80)
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="ALGORYTMY FAKTORYZACJI LICZB",
                               font=('Arial', 16, 'bold'), fg='white', bg='#333333')
        title_label.pack(expand=True)

        subtitle_label = tk.Label(header_frame, text="Rho Pollarda • Dixon • Porównanie",
                                  font=('Arial', 12), fg='#ecf0f1', bg='#333333',pady=10)
        subtitle_label.pack()

        # Główny kontener
        main_frame = tk.Frame(self.root, bg='#333333')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Panel sterowania
        control_frame = tk.LabelFrame(main_frame,
                                      font=('Arial', 11, 'bold'), bg='#333333', fg='white')
        control_frame.pack(fill='x', pady=(0, 10))

        # Liczba do faktoryzacji
        number_frame = tk.Frame(control_frame, bg='#333333')
        number_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(number_frame, text="Liczba do faktoryzacji:",
                 font=('Arial', 12, 'bold'), bg='#333333',fg='white').pack(side='left')

        self.number_entry = tk.Entry(number_frame, textvariable=self.number_var,
                                     font=('Arial', 11), width=25)
        self.number_entry.pack(side='left', padx=(10, 0))

        # Przykładowe liczby
        examples_frame = tk.Frame(control_frame, bg='#333333')
        examples_frame.pack(fill='x', padx=10, pady=(0, 10))

        tk.Label(examples_frame, text="Przykłady:",
                 font=('Arial', 12,'bold'), bg='#333333', fg='white').pack(side='left')

        examples = [1403, 8051, 143789, 982451]
        for example in examples:
            btn = tk.Button(examples_frame, text=str(example),
                            command=lambda x=example: self.number_var.set(str(x)),
                            font=('Arial', 12), bg='#222222',fg='white',
                            relief='flat', padx=8, pady=2)
            btn.pack(side='left', padx=(5, 0))

        # Wybór algorytmu
        algo_frame = tk.Frame(control_frame, bg='#333333')
        algo_frame.pack(fill='x', padx=12, pady=(0, 10))

        tk.Label(algo_frame, text="Algorytm:",
                 font=('Arial', 12, 'bold'), bg='#333333',fg='white').pack(side='left')

        algos = [
            ("Rho Pollarda", "pollard"),
            ("Dixon", "dixon"),
            ("Oba", "compare")
        ]

        for text, value in algos:
            rb = tk.Radiobutton(algo_frame, text=text, variable=self.algorithm_var,
                                value=value, font=('Arial', 12, 'bold'), bg='#333333',fg='white',
                                command=self.toggle_compare_options)
            rb.pack(side='left', padx=(15, 0))

        # Opcje
        options_frame = tk.Frame(control_frame, bg='#333333')
        options_frame.pack(fill='x', padx=10, pady=(0, 10))

        self.verbose_cb = tk.Checkbutton(options_frame, text="Szczegółowe kroki",
                                         variable=self.verbose_var, font=('Arial', 10, 'bold'), bg='#333333',fg='white'
                                         )
        self.verbose_cb.pack(side='left')

        self.compare_steps_cb = tk.Checkbutton(options_frame, text="Kroki porównania",
                                               variable=self.compare_steps_var, font=('Arial', 10,'bold'),
                                               bg='#333333',fg='white')
        self.compare_steps_cb.pack(side='left', padx=(15, 0))
        self.compare_steps_cb.configure(state='disabled')

        # Przyciski
        button_frame = tk.Frame(control_frame, bg='#333333')
        button_frame.pack(fill='x', padx=10, pady=(0, 10))

        self.run_button = tk.Button(button_frame, text="URUCHOM FAKTORYZACJĘ",
                                    command=self.run_factorization,
                                    font=('Arial', 11, 'bold'), bg='#222222', fg='white',
                                    relief='flat', padx=15, pady=6)
        self.run_button.pack(side='left')

        self.clear_button = tk.Button(button_frame, text="Wyczyść",
                                      command=self.clear_results,
                                      font=('Arial', 11), bg='#222222', fg='white',
                                      relief='flat', padx=15, pady=6)
        self.clear_button.pack(side='left', padx=(10, 0))

        # Panel wyników
        results_frame = tk.LabelFrame(main_frame, text="Wyniki",
                                      font=('Arial', 12, 'bold'), bg='#333333', fg='white')
        results_frame.pack(fill='both', expand=True)

        # Pole tekstowe na wyniki
        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                      font=('Consolas', 10),
                                                      bg='#333333', fg='#ecf0f1',
                                                      insertbackground='#ecf0f1',
                                                      wrap='word')
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)

        # Pasek statusu
        self.status_frame = tk.Frame(self.root, bg='#222222', height=30)
        self.status_frame.pack(fill='x', side='bottom')
        self.status_frame.pack_propagate(False)

        self.status_label = tk.Label(self.status_frame, text="Gotowy do pracy",
                                     font=('Arial', 12,'bold'), bg='#222222', fg='#ecf0f1')
        self.status_label.pack(side='left', padx=10, pady=3)

        self.progress = ttk.Progressbar(self.status_frame, mode='indeterminate')
        self.progress.pack(side='right', padx=10, pady=5, fill='x', expand=True)

        # Dodaj przykładową liczbę
        self.number_var.set("1403")

    def toggle_compare_options(self):
        """Włącza/wyłącza opcje związane z porównaniem"""
        if self.algorithm_var.get() == "compare":
            self.compare_steps_cb.configure(state='normal')
            self.verbose_cb.configure(state='disabled')
        else:
            self.compare_steps_cb.configure(state='disabled')
            self.verbose_cb.configure(state='normal')

    def append_result(self, text):
        """Dodaje tekst do pola wyników"""
        self.results_text.insert('end', text)
        self.results_text.see('end')
        self.root.update()

    def clear_results(self):
        """Czyści pole wyników"""
        self.results_text.delete(1.0, 'end')
        self.status_label.config(text="Wyniki wyczyszczone")

    def update_status(self, text):
        """Aktualizuje pasek statusu"""
        self.status_label.config(text=text)

    def run_factorization(self):
        """Uruchamia faktoryzację w osobnym wątku"""
        try:
            n = int(self.number_var.get().strip())
            if n <= 1:
                messagebox.showerror("Błąd", "Liczba musi być większa od 1")
                return
        except ValueError:
            messagebox.showerror("Błąd", "Podaj prawidłową liczbę całkowitą")
            return

        # Wyłącz przycisk i uruchom pasek postępu
        self.run_button.config(state='disabled')
        self.progress.start()
        self.clear_results()

        # Uruchom w osobnym wątku
        thread = threading.Thread(target=self.factorize_worker, args=(n,))
        thread.daemon = True
        thread.start()

    def factorize_worker(self, n):
        """Worker thread dla faktoryzacji"""
        try:
            algorithm = self.algorithm_var.get()
            verbose = self.verbose_var.get()
            compare_steps = self.compare_steps_var.get()

            self.append_result(f"{'=' * 60}\n")
            self.append_result(f"FAKTORYZACJA LICZBY: {n}\n")
            self.append_result(f"{'=' * 60}\n\n")

            if algorithm == "pollard":
                self.run_pollard_rho(n, verbose)
            elif algorithm == "dixon":
                self.run_dixon(n, verbose)
            elif algorithm == "compare":
                self.run_comparison(n, compare_steps)

        except Exception as e:
            self.append_result(f"❌ Błąd: {str(e)}\n")
        finally:
            # Przywróć interfejs
            self.root.after(0, self.restore_interface)

    def run_pollard_rho(self, n, verbose):
        """Uruchamia algorytm Rho Pollarda"""
        self.update_status("Uruchamianie Rho Pollarda...")

        callback = self.append_result if verbose else None
        pollard = PollardRho(callback=callback)

        start_time = time.time()
        factor = pollard.factorize(n)
        end_time = time.time()

        self.append_result(f"\n{'=' * 40}\n")
        self.append_result(f"WYNIKI ALGORYTMU RHO POLLARDA\n")
        self.append_result(f"{'=' * 40}\n")

        if factor:
            self.append_result(f"✅ Sukces! Znaleziony dzielnik: {factor}\n")
            self.append_result(f"📊 Sprawdzenie: {n} = {factor} × {n // factor}\n")
        else:
            self.append_result(f"❌ Nie znaleziono dzielnika\n")

        self.append_result(f"⏱️  Czas wykonania: {end_time - start_time:.6f} s\n")
        self.append_result(f"🔄 Liczba iteracji: {len(pollard.steps)}\n")

        self.update_status(f"Rho Pollarda zakończony - {'sukces' if factor else 'brak wyniku'}")

    def run_dixon(self, n, verbose):
        """Uruchamia algorytm Dixona"""
        self.update_status("Uruchamianie Dixona...")

        callback = self.append_result if verbose else None
        dixon = Dixon(callback=callback)

        start_time = time.time()
        factor = dixon.factorize(n)
        end_time = time.time()

        self.append_result(f"\n{'=' * 40}\n")
        self.append_result(f"WYNIKI ALGORYTMU DIXONA\n")
        self.append_result(f"{'=' * 40}\n")

        if factor:
            self.append_result(f"✅ Sukces! Znaleziony dzielnik: {factor}\n")
            self.append_result(f"📊 Sprawdzenie: {n} = {factor} × {n // factor}\n")
        else:
            self.append_result(f"❌ Nie znaleziono dzielnika\n")

        self.append_result(f"⏱️  Czas wykonania: {end_time - start_time:.6f} s\n")

        self.update_status(f"Dixon zakończony - {'sukces' if factor else 'brak wyniku'}")

    def run_comparison(self, n, show_steps):
        """Uruchamia porównanie algorytmów"""
        self.update_status("Porównywanie algorytmów...")

        runs = 3
        results = {'pollard_rho': {'times': [], 'factors': [], 'steps': []},
                   'dixon': {'times': [], 'factors': [], 'steps': []}}

        self.append_result(f"PORÓWNANIE ALGORYTMÓW ({runs} przebiegów każdy)\n")
        self.append_result(f"{'=' * 60}\n\n")

        # Test Pollard Rho
        self.append_result("🔵 TESTOWANIE RHO POLLARDA\n")
        self.append_result(f"{'-' * 40}\n")
        for i in range(runs):
            self.append_result(f"\nPrzebieg {i + 1}/{runs}:\n")
            self.append_result(f"{'-' * 20}\n")

            pollard = PollardRho(callback=self.append_result if show_steps else None)
            start_time = time.time()
            factor = pollard.factorize(n)
            end_time = time.time()

            results['pollard_rho']['times'].append(end_time - start_time)
            results['pollard_rho']['factors'].append(factor)
            results['pollard_rho']['steps'].append(len(pollard.steps))

            if not show_steps:
                self.append_result(f"Status: {'✅' if factor else '❌'}\n")
            self.append_result(f"Czas: {end_time - start_time:.6f}s\n")
            self.append_result(f"Liczba kroków: {len(pollard.steps)}\n")

        # Test Dixon
        self.append_result("\n🔴 TESTOWANIE DIXONA\n")
        self.append_result(f"{'-' * 40}\n")
        for i in range(runs):
            self.append_result(f"\nPrzebieg {i + 1}/{runs}:\n")
            self.append_result(f"{'-' * 20}\n")

            dixon = Dixon(callback=self.append_result if show_steps else None)
            start_time = time.time()
            factor = dixon.factorize(n)
            end_time = time.time()

            results['dixon']['times'].append(end_time - start_time)
            results['dixon']['factors'].append(factor)
            results['dixon']['steps'].append(0)  # Dixon nie ma kroków w tej implementacji

            if not show_steps:
                self.append_result(f"Status: {'✅' if factor else '❌'}\n")
            self.append_result(f"Czas: {end_time - start_time:.6f}s\n")

        # Podsumowanie
        self.append_result(f"\n{'=' * 30}\n")
        self.append_result(f"PODSUMOWANIE PORÓWNANIA\n")
        self.append_result(f"{'=' * 30}\n")

        for algo_name, data in results.items():
            algo_display = "🔵 Rho Pollarda" if algo_name == "pollard_rho" else "🔴 Dixon"
            times = data['times']
            factors = data['factors']
            steps = data['steps']

            successful_runs = sum(1 for f in factors if f is not None)

            self.append_result(f"\n{algo_display}:\n")
            self.append_result(f"  📊 Skuteczność: {successful_runs}/{runs} ({successful_runs / runs * 100:.1f}%)\n")
            self.append_result(f"  ⏱️  Średni czas: {np.mean(times):.6f} s\n")
            self.append_result(f"  ⚡ Min/Max: {min(times):.6f}s / {max(times):.6f}s\n")

            if algo_name == "pollard_rho":
                self.append_result(f"  🔄 Średnia liczba kroków: {np.mean(steps):.1f}\n")

            if successful_runs > 0:
                successful_factors = [f for f in factors if f is not None]
                self.append_result(f"  🎯 Znalezione dzielniki: {set(successful_factors)}\n")

        self.update_status("Porównanie zakończone")

    def restore_interface(self):
        """Przywraca interfejs po zakończeniu obliczeń"""
        self.run_button.config(state='normal')
        self.progress.stop()


def main():
    """Główna funkcja GUI"""
    root = tk.Tk()
    app = FactorizationGUI(root)

    root.eval('tk::PlaceWindow . center')

    root.mainloop()


if __name__ == "__main__":
    main()