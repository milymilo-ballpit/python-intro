import numpy as np
import pandas as pd
from pymcdm.methods import TOPSIS, SPOTIS
from pymcdm.normalizations import minmax_normalization

# Sztuczne dane dotyczące wyboru laptopa:
# Wiersze: Modele Laptopów
# Kolumny:
# - Cena,
# - Wydajność (Wynik jakiegoś nenchmarku)
# - Czas pracy na baterii (h),
# - Waga (kg)

decision_matrix = np.array([
    [3000, 4500, 8, 1.5], # Model A
    [3500, 5000, 6, 2.1], # Model B
    [2800, 4300, 10, 1.6], # Model C
    [3200, 4800, 9, 1.7], # Model D
    [3100, 4600, 7, 1.4] # Model E
])

# Istotność (waga) parametrów:
# - cena jest najważniejszym kryterium (40%)
# - wydajność na 2 miejscu (30%)
# - czas pracy na baterii na 3 (20%)
# - waga na 4 (10%)
weights = np.array([0.4, 0.3, 0.2, 0.1])

# Kryteria (typ) parametru:
# - dążymy do najniższej ceny i wagi (koszt)
# - najwyższej wydajności i czasu pracy na baterii (korzyść)
types = np.array([-1, 1, 1, -1])

# Normalizacja:
# Przekształca wartości do wspólnej skali w zależności czy cecha jest
# kosztem (dążymy do minimalizacji) czy korzyścią (dążymy do maksymalizacji)
normalized_matrix = np.zeros(decision_matrix.shape)
for i in range(decision_matrix.shape[1]):
    normalized_matrix[:, i] = minmax_normalization(decision_matrix[:, [i]], cost=(types[i] == -1)).flatten()

# TOPSIS
topsis = TOPSIS()
topsis_ranking = topsis(normalized_matrix, weights, types)

# SPOTSIS
bounds = np.vstack((decision_matrix.min(axis=0), decision_matrix.max(axis=0))).T
spotis = SPOTIS(bounds=bounds)
spotis_ranking = spotis(decision_matrix, weights, types)

results_df = pd.DataFrame({
    'Laptop': ['Model A', 'Model B', 'Model C', 'Model D', 'Model E'],
    'TOPSIS': topsis_ranking,
    'SPOTIS': spotis_ranking
})

# Wyświetlamy wyniki posortowane po TOPSIS malejąco (od najlepszych)
print(results_df.sort_values(by='TOPSIS', ascending=False))
