% I: FILMY

% movie(Tytul, Gatunek, Ocena, RokProdukcji, Rezyser).
movie('The Shawshank Redemption', drama, 9.3, 1994, 'Frank Darabont').
movie('The Godfather', drama, 9.2, 1972, 'Francis Ford Coppola').
movie('The Dark Knight', action, 9.0, 2008, 'Christopher Nolan').
movie('The Godfather: Part II', drama, 9.0, 1974, 'Francis Ford Coppola').
movie('12 Angry Men', drama, 9.0, 1957, 'Sidney Lumet').
movie('The Return of the King', adventure, 9.0, 2003, 'Peter Jackson').
movie('Schindler\'s List', biography, 9.0, 1993, 'Steven Spielberg').
movie('Pulp Fiction', crime, 8.9, 1994, 'Quentin Tarantino').
movie('The Fellowship of the Ring', adventure, 8.8, 2001, 'Peter Jackson').
movie('The Good, the Bad & the Ugly', western, 8.8, 1966, 'Sergio Leone').
movie('Forrest Gump', drama, 8.8, 1994, 'Robert Zemeckis').
movie('The Two Towers', adventure, 8.8, 2002, 'Peter Jackson').
movie('Fight Club', drama, 8.8, 1999, 'David Fincher').
movie('Inception', sci_fi, 8.8, 2010, 'Christopher Nolan').
movie('The Empire Strikes Back', adventure, 8.7, 1980, 'Irvin Kershner').
movie('The Matrix', sci_fi, 8.7, 1999, 'Lana Wachowski & Lilly Wachowski').
movie('Goodfellas', crime, 8.7, 1990, 'Martin Scorsese').
movie('Interstellar', sci_fi, 8.7, 2014, 'Christopher Nolan').
movie('One Flew Over the Cuckoo\'s Nest', drama, 8.7, 1975, 'Milos Forman').
movie('Se7en', thriller, 8.6, 1995, 'David Fincher').
movie('It\'s a Wonderful Life', drama, 8.6, 1946, 'Frank Capra').
movie('The Silence of the Lambs', thriller, 8.6, 1991, 'Jonathan Demme').
movie('Seven Samurai', adventure, 8.6, 1954, 'Akira Kurosawa').
movie('Saving Private Ryan', drama, 8.6, 1998, 'Steven Spielberg').
movie('City of God', drama, 8.6, 2002, 'Fernando Meirelles').

movies_by_genre(Genre, MovieList) :-
    findall(Title, movie(Title, Genre, _, _, _), MovieList).

movies_by_rating(MinRating, MovieList) :-
    findall(Title,
            ( movie(Title, _, Rating, _, _), Rating >= MinRating ),
            MovieList).

movies_by_director(Director, MovieList) :-
    findall(Title, movie(Title, _, _, _, Director), MovieList).

older_than(YearLimit, MovieList) :-
    findall(Title,
            ( movie(Title, _, _, ReleaseYear, _), ReleaseYear < YearLimit ),
            MovieList).

newer_or_equal(YearLimit, MovieList) :-
    findall(Title,
            ( movie(Title, _, _, ReleaseYear, _), ReleaseYear >= YearLimit ),
            MovieList).

top_genre(Genre, MinRating, MovieList) :-
    findall(Title,
            ( movie(Title, Genre, Rating, _, _), Rating >= MinRating ),
            MovieList).

% CZĘŚĆ II: DRZEWO GENEALOGICZNE

% Osoby
male('Jan').
male('Piotr').
male('Andrzej').
male('Marek').
male('Tomasz').
male('Paweł').
male('Krzysztof').
male('Adam').
male('Robert').
male('Łukasz').
male('Patryk').
male('Mateusz').

female('Anna').
female('Maria').
female('Katarzyna').
female('Ewa').
female('Magdalena').
female('Agnieszka').
female('Monika').
female('Joanna').
female('Beata').
female('Natalia').
female('Paulina').
female('Karolina').

% Relacje
parent('Jan', 'Piotr').
parent('Anna', 'Piotr').
parent('Jan', 'Maria').
parent('Anna', 'Maria').
parent('Piotr', 'Marek').
parent('Ewa', 'Marek').
parent('Piotr', 'Katarzyna').
parent('Ewa', 'Katarzyna').
parent('Andrzej', 'Tomasz').
parent('Maria', 'Tomasz').
parent('Andrzej', 'Monika').
parent('Maria', 'Monika').
parent('Marek', 'Paweł').
parent('Magdalena', 'Paweł').
parent('Marek', 'Agnieszka').
parent('Magdalena', 'Agnieszka').
parent('Tomasz', 'Krzysztof').
parent('Joanna', 'Krzysztof').
parent('Tomasz', 'Natalia').
parent('Joanna', 'Natalia').
parent('Monika', 'Adam').
parent('Robert', 'Adam').
parent('Monika', 'Beata').
parent('Robert', 'Beata').
parent('Paweł', 'Łukasz').
parent('Paulina', 'Łukasz').
parent('Paweł', 'Karolina').
parent('Paulina', 'Karolina').

% Reguły
mother(Mother, Child) :-
    female(Mother),
    parent(Mother, Child).

father(Father, Child) :-
    male(Father),
    parent(Father, Child).

sibling(Person1, Person2) :-
    parent(Parent, Person1),
    parent(Parent, Person2),
    Person1 \= Person2.

grandparent(Grandparent, Grandchild) :-
    parent(Grandparent, Parent),
    parent(Parent, Grandchild).

ancestor(Ancestor, Descendant) :-
    parent(Ancestor, Descendant).
ancestor(Ancestor, Descendant) :-
    parent(Ancestor, Intermediate),
    ancestor(Intermediate, Descendant).

cousin(Person, Cousin) :-
    parent(Parent1, Person),
    parent(Parent2, Cousin),
    sibling(Parent1, Parent2),
    Person \= Cousin.

:- initialization(main).

main :-
    format('=== FILMY (IMDB Top 25) ===~n'),
    movies_by_genre(adventure, AdventureMovies),
    format('Filmy przygodowe: ~w~n', [AdventureMovies]),

    movies_by_rating(9.0, HighRatedMovies),
    format('Filmy z oceną >= 9.0: ~w~n', [HighRatedMovies]),

    movies_by_director('Christopher Nolan', NolanMovies),
    format('Filmy Christophera Nolana: ~w~n', [NolanMovies]),

    older_than(2000, Pre2000Movies),
    format('Filmy przed rokiem 2000: ~w~n', [Pre2000Movies]),

    top_genre(drama, 8.8, TopDramaMovies),
    format('Filmy dramatyczne z oceną >= 8.8: ~w~n', [TopDramaMovies]),

    format('\n=== DRZEWO GENEALOGICZNE ===~n'),
    findall(Child,
            mother('Anna', Child),
            ChildrenOfAnna),
    format('Dzieci Anny: ~w~n', [ChildrenOfAnna]),

    findall(Sibling,
            sibling('Piotr', Sibling),
            SiblingsOfPiotr),
    format('Rodzeństwo Piotra: ~w~n', [SiblingsOfPiotr]),

    findall(Grandchild,
            grandparent('Jan', Grandchild),
            GrandchildrenOfJan),
    format('Wnuki Jana: ~w~n', [GrandchildrenOfJan]),

    findall(Descendant,
            ancestor('Jan', Descendant),
            DescendantsOfJan),
    format('Potomkowie Jana: ~w~n', [DescendantsOfJan]),

    findall(Cousin,
            cousin('Marek', Cousin),
            CousinsOfMarek),
    format('Kuzyni Marka: ~w~n', [CousinsOfMarek]),

    halt.
