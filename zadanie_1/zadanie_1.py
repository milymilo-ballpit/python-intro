import random

names = ["Ania", "Bartek", "Kasia", "Miłosz"]
ages = [20, 28, 26, 24]

# https://docs.python.org/3.12/library/functions.html#zip
# Złączenie kolejnych elementów z list `names` oraz `ages` przy użyciu funkcji wbudowanej `zip()`.
#
# Funkcja zip przyjmuje 2 dowolne kolekcje jako argumenty pozycyjne i zwraca iterator krotek będących połączeniem
# elementów z obu kolekcji na danym indeksie e.g. ("Ania", 20)
#
# `zip()` przyjmuje również keyword argument `strict` - boolean, który spowoduje zwrócenie wyjątku jeżeli
# kolekcje nie są równe. W przeciwnym (domyślnym) wypadku funkcja zwróci iterator kolekcji o długości najkrótszej
# kolekcji wejściowej.
#
# Podniesiony wyjątek to `ValueError` -

names_with_ages = list(zip(names, ages, strict=True))
print(names_with_ages)

# https://docs.python.org/3.12/library/random.html
# Moduł random implementuje fukcjonalność związaną z szerokopojetą losowością.
# Znajdziemy tutaj funkcje pozwalające generować różne losowe typy danych, oraz manipulować
# istniejącymi danymi wykorzystując losowość.
#
# Co ważne, random nie jest losowy tylko pseudo-losowy. Korzysta z PRNG wykorzystującego seed
# (domyślnie os.urandom) i nie powinien być wykorzystywany do bezpiecznego losowania danych tak jak
# np. przy hasłach. Losowość w module random jest całkowicie oparta na wartości seeda i może zostać
# odtworzona.
#
# https://docs.python.org/3.12/library/random.html#random.sample
# https://docs.python.org/3.12/library/random.html#random.randint
#
# Wykorzystanie funkcji `sample()` oraz `randint` z modułu `random`
# `sample` - zwraca listę (podzbiór) o podanej długości z danej listy
# `randint` - losuje liczbę całkowitą w podanym zakresie (a <= N <= b)
#
# Losowanie dwóch pod-list z list `names` oraz `ages`, o losowej długości
# Możliwe (bardzo prawdopodobne) jest wylosowanie dwóch list o różnej długości
# co spowoduje ww. wyjątek z użyciem `zip()`
random_names = random.sample(names, random.randint(0, len(names)))
random_ages = random.sample(ages, random.randint(0, len(ages)))

try:
    random_names_with_ages = list(zip(random_names, random_ages, strict=True))
except ValueError:
    print("Wylosowane listy nie są równej długości!")
else:
    print(random_names_with_ages)