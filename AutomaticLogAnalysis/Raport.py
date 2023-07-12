from Dane_do_raportu import *
import pprint

def generuj_raport(path):

    logi_cale = wczytywanie(path)
    wadliwe = wady(wczytywanie(path))
    procenty = procent_wad(wadliwe, logi_cale)
    raport_czas = czas_rap(logi_cale, wadliwe)
    temperatura = temperatury(logi_cale, wadliwe)
    problemy = problem(logi_cale, wadliwe)

    raport = {
        "wadliwe_logi":wadliwe,
        "procent_wadliwych_logow":procenty,
        "czas_trwania_raportu":raport_czas,
        "temperatura":temperatura,
        "najdluzszy_czas_przegrzania":"brak",
        "liczba_okresow_przegrzania":"brak",
        "problemy":problemy,
    }

    return raport

pretty = pprint.PrettyPrinter(sort_dicts=False)
pretty.pprint(generuj_raport("logi_03.txt"))
