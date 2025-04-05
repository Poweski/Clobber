## EN
Clobber is a board game for two players played on a board of any size (5x6 by default). Players take turns moving to adjacent squares occupied by the opponent and capturing their disks. The game ends when neither player can make a move - the player who made the last move wins.

The project implements both the classic Minimax algorithm and the Alpha-Beta pruning version, with the ability to set the maximum search depth. Each player has three different heuristics for evaluating the state of the game, which can be adaptively changed during the game. The program allows for playing a game between two AIs with independent strategies.

The startup screen is loaded from a file redirected to standard input. The program outputs the final state of the board, the number of rounds and the winner, and to stderr - the number of visited nodes and the algorithm's runtime.

## PL
Clobber to gra planszowa dla dwóch graczy rozgrywana na planszy o dowolnym rozmiarze (domyślnie 5x6). Gracze wykonują ruchy naprzemiennie, poruszając się na sąsiadujące pola zajęte przez przeciwnika i zbijając jego krążki. Gra kończy się, gdy żaden z graczy nie może wykonać ruchu — wygrywa gracz, który wykonał ostatni ruch.

Projekt implementuje zarówno klasyczny algorytm Minimax, jak i wersję z przycinaniem Alpha-Beta, z możliwością ustawienia maksymalnej głębokości przeszukiwania. Każdy gracz posiada trzy różne heurystyki oceny stanu gry, które mogą być adaptacyjnie zmieniane w trakcie rozgrywki. Program umożliwia przeprowadzenie gry pomiędzy dwoma AI z niezależnymi strategiami.

Plansza startowa wczytywana jest z pliku przekierowanego do standardowego wejścia. Na wyjściu program wypisuje końcowy stan planszy, liczbę rund i zwycięzcę, a na stderr — liczbę odwiedzonych węzłów oraz czas działania algorytmu.
