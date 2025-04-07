---
task: xxx
authors:
  - name: xxx
    email: xxx
    album: xxx
    group: xxx
toc: false
---

#### 1. Instalacja biblioteki `pymcdm`

Biblioteka została zainstalowana przy użyciu managera środowiska `uv`

```bash
uv add pymcdm numpy pandas
```

#### 2. Przygotowanie danych

Przygotowano (sztuczny) zestaw danych reprezentujący różne modele laptopów

Każdy model jest opisany przez:

- Cenę (pln / koszt)
- Wydajność (wynik hipotetycznego benchmarku / korzyść)
- Czas pracy na baterii (h / korzyść)
- Wagę (kg / koszt)

```python
--8<-- "main.py:14:23"
```

Dostosowano istotność (wagi) poszczególnych parametrów:

- Cena - 40%
- Wydajność - 30%
- Czas pracy na baterii - 20%
- Waga - 10%

```python
--8<-- "main.py:29:30"
```

Zdefiniowano również typy parametrów:

- Korzyści, do którch **maksymalizacji** dążymy (więcej=lepiej)
- Koszty, do których **minimalizacji** dążymy (mniej=lepiej)

```python
--8<-- "main.py:34:35"
```

/// break

#### 3. Normalizacja

Przygotowane dane zostały znormalizowane za pomocą funckji `minmax_normalization` z biblioteki `pymcdm`:

```python
--8<-- "main.py:39:44"
```

#### 4. Wykorzystanie metod decyzyjnych

Zgodnie z zadaniem wykorzystano 2 metody `TOPSIS` oraz `SPOTIS`:

```python
--8<-- "main.py:46:61"
```

#### 5. Wyniki

Wyniki zaprezentowano wypisując w terminalu dataframe posortowany malejąco po wyniku `TOPSIS`:

| Laptop  | TOPSIS   | SPOTIS   |
|---------|----------|----------|
| Model B | 0.718271 | 0.700000 |
| Model D | 0.629321 | 0.407143 |
| Model E | 0.394427 | 0.492857 |
| Model A | 0.314899 | 0.442857 |
| Model C | 0.285714 | 0.328571 |

Obie metody wskazują Model B jako najlepszy wybór pomimo najwyższej ceny (która ma również najwyższą wagę), oznacza to
że przeskok ceny musi być znacząco uzasadniony biorąc pod uwagę pozostałe kryteria.