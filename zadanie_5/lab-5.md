---
task: xxx
authors:
  - name: xxx
    email: xxx
    album: xxx
    group: xxx
toc: false
---

#### Wybór bibliotek

Wybrana do zadania tematyka to interakcja za pomocą pythona z klastrem Kubernetes.

Znalazłem kilka bibliotek, które oferują API / SDK do interakcji z API k8s (a.k.a Kubernetes):

1. [`kubernetes`](https://github.com/kubernetes-client/python)
2. [`kubernetes-asyncio`](https://github.com/tomplus/kubernetes_asyncio)
3. [`kr8s`](https://github.com/kr8s-org/kr8s)
4. [`lightkube`](https://github.com/gtsystem/lightkube)

Wszystkie opisywane biblioteki są na chwilę pisania raportu aktywnie utrzymywane.

#### Porównanie

/// no-break
`kubernetes` - ⭐ 7100

- Python: 3.6 - 3.11
- Dokumentacja: [https://kubernetes.readthedocs.io/en/latest/](https://kubernetes.readthedocs.io/en/latest/)

**Zalety:**

1. Jest to oficjalny klient, który najprawdopodobniej będzie wspierany tak długo, jak sam kuberentes.
2. Wszelkie konieczne zmiany będą wprowadzane równolegle ze zmianami w samym kubernetes.

**Wady:**

1. Nie wspiera asynchroniczności, cały klient jest w pełni synchroniczny, co w konkretnym przypadku interakcji z
   klastrem bywa problematyczne. W praktyce często pojawia się potrzeba wykonania kodu, który będzie oczekiwał na
   jakiegoś rodzaju zmianę stanu lub zdarzenie (watch / event). W przypadku biblioteki w pełni synchronicznej zwykle
   sprowadza się do wykorzystania wątków, które są mniej eleganckie i trudniejsze w utrzymaniu niż kod asynchroniczny.
2. Całe SDK jest generowane automatycznie z definicji OpenAPI - efektywnie kod posiada bardzo wiele, często zbędnych,
   abstrakcji, z których musimy korzystać. Całość wygląda syntetycznie, rozwlekle (*verbose*) i mało elegancko.

///

/// no-break
`kubernetes-asyncio` - ⭐ 389

- Python: 3.6 - 3.11
- Dokumentacja: [https://kubernetes-asyncio.readthedocs.io/en/latest/](https://kubernetes-asyncio.readthedocs.io/en/latest/)

**Zalety:**

1. Dodaje możliwość korzystania z oficjalnego klienta w sposób asynchroniczny
2. Również jest generowana w sposób automatyczny, tak więc powinna zachować podobny poziom kompatybilności

**Wady:**

1. Nie wspiera operacji synchronicznych - nie możemy korzystać z obu wersji w zależności od potrzeby.
2. Efektywnie kod wygenerowany automatycznie z dodaną funkcjonalnością asynchroniczną jest jeszcze bardziej rozwlekły.

///

/// no-break
`kr8s` - ⭐ 892

- Python: 3.9 - 3.12
- Dokumentacja: [https://docs.kr8s.org/en/latest/](https://docs.kr8s.org/en/latest/)

**Zalety:**

1. W przeciwieństwie do pozostałych nie skupia się na odwzorowaniu struktury API kubernetes, lecz na odwzorowaniu
   komendy `kubectl` (wykorzystywanej do interakcji z klastrem). Zmiana podejścia sprawia, że biblioteka
   jest dużo bardziej intuicyjna.
2. Wspiera jednocześnie operacje asynchroniczne oraz asynchroniczne.
3. Napisana w całości ręcznie - API jest intuicyjne, zwięzłe i eleganckie.
4. Pomimo że jest to klient nieoficjalny, jest względnie popularny i ryzyko porzucenia projektu bez jego kontynuacji
   jest niskie.

**Wady:**

1. Zmiana podejścia i porzucenie założenia dokładnego odwzorowania API może sprawić, że pewne funkcjonalności będą
   niemożliwe do wykorzystania.
2. Jest to klient nieoficjalny, który na dodatek nie jest generowany automatycznie - wszelkie zmiany w API kuberentes
   mogą zająć dłuższą chwilę, aby zostać wdrożone.

///

/// no-break
`lightkube` - ⭐ 116

- Python: 3.8 - 3.13
- Dokumentacja: [https://lightkube.readthedocs.io/en/latest/](https://lightkube.readthedocs.io/en/latest/)

**Zalety**:

1. Lightkube odwzorowuje API - jednak w sposób bardziej zwięzły i elegancki niż oficjalny klient.
2. Wspiera jednocześnie operacje asynchroniczne oraz asynchroniczne.
3. Z uwagi na częściowe generowanie automatyczne, wdrożenie zmian w API k8s może być szybsze niż w przypadku `kr8s`,
   zachowując względnie elegancką strukturę.

**Wady**:

1. Podobnie jak `kr8s` jest to klient nieoficjalny, który za pewien czas może zostać porzucony.
2. Pomimo iż API jest bardziej eleganckie niż w przypadku `kubernetes`, to pozostaje bardziej rozwlekłe niż `kr8s`
3. Najmniej popularna z wymienionych bibliotek (największe ryzyko porzucenia bez kontynuacji)

///

/// break

/// no-break

#### Przykłady

W ramach przykładu zaprezentuję kod, który ma za zadanie znaleźć w danej przestrzeni nazw (namespace) wszystkie pody z
daną wartością etykiety. Aby przygotować klaster pod test musimy stworzyć namespace oraz trzy repliki prostego
deploymentu, który będzie zawierał w sobie kontener z nginx:

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: test
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: test
  labels:
    test-label: test-value
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
        test-label: test-value
    spec:
      containers:
      - name: nginx
        image: nginx
EOF
```

Efektem powinno być utworzenie namespace `test`, w nim deploymentu oraz 3 podów z etykietą `test-label=test-value`:

```bash
$ kubectl get pods -n test --show-labels
NAME                              (***) LABELS
nginx-deployment-745d4587cd-66ph7 (***) test-label=test-value
nginx-deployment-745d4587cd-tjjs9 (***) test-label=test-value
nginx-deployment-745d4587cd-vklm8 (***) test-label=test-value
```

///

/// no-break
**kubernetes:**

```python
--8<-- "src/example-kubernetes.py"
```

///

/// break

/// no-break
**kubernetes-asyncio:**

```python
--8<-- "src/example-kubernetes-asyncio.py"
```

///

/// break

/// no-break
**kr8s:**

```python
--8<-- "src/example-kr8s.py"
```

///

/// break

/// no-break
**lightkube:**

```python
--8<-- "src/example-lightkube.py"
```

///

/// break

#### Podsumowanie

Tak jak widać na przedstawionych przykładach, kod korzystający z oficjalnego klienta kubernetes jest zdecydowanie
najbardziej *opisowy*. Musimy stworzyć obiekty api o nazwach `CoreV1Api` oraz `AppsV1Api` oraz skorzystać z metod takich
jak `v1.list_namespaced_pod` oraz `apps.patch_namespaced_deployment_scale`, który wymaga podania jako parametr `body`
obiektu `client.V1Scale(spec=client.V1ScaleSpec(...))`. W przypadku `kubernetes-asyncio` wszystko należy opatrzyć
dodatkowo `await` - co akurat jest naturalne.

Porównując do `lightkube` widzimy tutaj pewne pokrewieństwo - jednak korzystamy z nieco bardziej intuicyjnych metod
`Deployment.Scale()` z parametrami `ObjectMeta()` oraz `ScaleSpec()` zamiast tworzenia wielokrotnie zagnieżdżonych
struktur. Reprezentacja API pozostaje, jednak zrealizowana nieco inaczej. Przy pisaniu przykładów zauważyłem wadę
biblioteki `lightkube` jaką jest bardzo duża ilość importów. `kubernetes` wystawia te obiekty jako właściwość klienta co
wydaje mi się nieco lepszym rozwiązaniem - miałem problem np. ze znalezieniem skąd właściwie zaimportować model `Pod`.

Finalnie, `kr8s` odbiega od założeń pozostałych - czyniąc kod dużo bardziej zwięzłym czytelnym i intuicyjnym. Obiekty
Kubernetes potrafią być bardzo duże - tak więc zrezygnowanie z tak dokładnego typowania na rzecz przekazywania
specyfikacji jako słowniki wydaje mi się uzasadnione. W podobny sposób robi to z resztą `kubectl` czytając specyfikację
w yamlu - tam nic nie weryfikuje dokładnej struktury.

