# VRPTW-App

Do gotowego algorytmu dodałem trzy metody GET:

*- solution_cost_json - zwraca wynik algorytmu ("zminimalizowany koszt")*

- typ: int 
- Przykładowy wynik: 71


*- solution_routes_json - zwraca listę pojazd oraz liste zwiedzonych przez niego punktów*

- typ: słownik
- Przykładowy wynik:
{
    "Vehicle 1": [
        0,
        9,
        14,
        16,
        0
    ],
    "Vehicle 2": [
        0,
        7,
        1,
        4,
        3,
        0
    ]
}

*- solution_full_json - zwraca wszystkie dane tj. wynik algorytmu, czas końcowy, czas dla poszczególnych tras i dokładniejszy opis tracy pojazdów*

- typ: słownik
- Przykładowy wynik:
{
    "Final cost": 71,
    "Total time": 82,
    "Vehicle 1": [
        {
            "Route and time windows": "0 Time(0,0) -> 9 Time(2,3) -> 14 Time(7,8) -> 16 Time(11,11) -> 0 Time(18,18)\n"
        },
        {
            "Route time": 18
        }
    ],
    "Vehicle 2": [
        {
            "Route and time windows": "0 Time(0,0) -> 7 Time(2,4) -> 1 Time(7,11) -> 4 Time(10,13) -> 3 Time(16,16) -> 0 Time(24,24)\n"
        },
        {
            "Route time": 24
        }
    ]
}
