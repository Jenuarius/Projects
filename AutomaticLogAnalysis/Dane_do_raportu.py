import re
import datetime

def wczytywanie(log):
    logi01 = open(log)
    logi01_list = []
    for line in logi01:
        logi01_list.append(line.strip())

    logi01.close()
    return logi01_list

def wady(logi01_list):

    wadliwe_logi = []

    for rekord in logi01_list:
        flag_d = False
        log2 = rekord[16:]
        log3 = rekord[0:16]
        temp_spr = re.search('\s\d\d\d[C]|\s\d\d[C]|\s\d\d\d\.\d[C]|\s\d\d\.\d[C]|\s?!-\d\d[C]', log2)

        try:
            data_spr = datetime.datetime.strptime(log3, "%Y-%m-%d %H:%M")
        except ValueError:
            flag_d = True

        if temp_spr == None or flag_d == True:
            wadliwe_logi.append(rekord)


    return wadliwe_logi


def procent_wad(wadliwe, logi_cale):

    wadliwe_el = len(wadliwe)
    logi_cale_el = len(logi_cale)
    procent = wadliwe_el / logi_cale_el * 100
    zaok_procent = "%.1f" % procent
    return zaok_procent


def czas_rap(logi_cale, wadliwe):

    wszystkie_logi = []
    logi_bez_zaklocen = []
    roznica_blad = 0

    for rekord in wadliwe:
        wszystkie_logi.append(rekord)

    for rekord2 in logi_cale:
        wszystkie_logi.append(rekord2)

    for rekord3 in wszystkie_logi:
        if wszystkie_logi.count(rekord3) == 1:
            logi_bez_zaklocen.append(rekord3)

    logi_spr = len(logi_bez_zaklocen)

    if logi_spr == 0:
        return roznica_blad

    skrajne_daty = logi_bez_zaklocen[0:1] + logi_bez_zaklocen[-1:]
    skrajne_daty2 = []

    for rekord4 in skrajne_daty:
        wycinek = rekord4[0:16]
        skrajne_daty2.append(wycinek)

    data_format = "%Y-%m-%d %H:%M"
    data1 = datetime.datetime.strptime(skrajne_daty2[0], data_format)
    data2 = datetime.datetime.strptime(skrajne_daty2[-1], data_format)
    roznica = data2 - data1
    roznica_min = roznica.seconds // 60


    return roznica_min


def temperatury(logi_cale, wadliwe):

    wszystkie_logi = []
    logi_bez_zaklocen = []

    for rekord in logi_cale:
        wszystkie_logi.append(rekord)

    for rekord2 in wadliwe:
        wszystkie_logi.append(rekord2)

    for rekord3 in wszystkie_logi:
        if wszystkie_logi.count(rekord3) == 1:
            logi_bez_zaklocen.append(rekord3)

    logi_spr = len(logi_bez_zaklocen)
    logi_temp_c = []

    for rekord4 in logi_bez_zaklocen:
        log_c = rekord4[17:]
        logi_temp_c.append(log_c)

    logi_temp = [element[:-1] for element in logi_temp_c]

    dec_max_temp = 0
    dec_min_temp = 0
    dec_sr_temp = 0

#MAX
    temp_float = [float(element) for element in logi_temp]

    if logi_spr == 0 or logi_spr == 1:
        dec_max_temp = None
    else:
        max_temp = max(temp_float)
        dec_max_temp = round(max_temp, 1)

#MIN
    if logi_spr == 0 or logi_spr == 1:
        dec_min_temp = None
    else:
        min_temp = min(temp_float)
        dec_min_temp = round(min_temp, 1)

#SREDNIA
    if logi_spr == 0 or logi_spr == 1:
        dec_sr_temp = None
    else:
        sr_temp = sum(temp_float) / len(temp_float)
        dec_sr_temp = round(sr_temp, 1)

    slownik = {
        "max":dec_max_temp,
        "min":dec_min_temp,
        "srednia":dec_sr_temp,
    }

    return slownik

def problem(logi_cale, wadliwe):

    zaklocenia = False
    logi_cale_el = len(logi_cale)
    wadliwe_el = len(wadliwe)
    proc_wad = 0

    if wadliwe_el == 0:
        zaklocenia = False
    else:
        proc_wad = logi_cale_el / wadliwe_el * 100

    if proc_wad > 10:
        zaklocenia = True


    slownik = {
        "wysoki_poziom_zaklocen_EM":zaklocenia,
        "wysokie_ryzyko_uszkodzenia_silnika_z_powodu_temperatury":"brak",
    }

    return slownik