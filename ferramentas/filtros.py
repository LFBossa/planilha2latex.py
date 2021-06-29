from datetime import date, time, datetime
import locale 
locale.setlocale(locale.LC_TIME, "pt_BR.utf8")

MAPA_DATAHORA = {
    "AAAA": "%Y",
    "AA": "%y",
    "MM": "%m",
    "mmm": "%b",
    "mês": "%B",
    "DD": "%d",
    "HH": "%H",
    "mm": "%M",
    "ds": "%a",
    "dia": "%A"
}

_D = lambda x: str(x.day)
_Ds =  lambda x: x.strftime("%a").capitalize()
_Dia = lambda x: x.strftime("%A").capitalize()
_Mes = lambda x: x.strftime("%B").capitalize()
_Diafeira = lambda x: _Dia(x)+"-feira" if x.weekday() < 5 else _Dia(x)
_diafeira = lambda x: _Diafeira(x).lower()

MAPA_DATAHORA_EXTRA = {
    "Mês": _Mes,
    "Ds": _Ds,
    "Dia-feira": _Diafeira, 
    "Dia": _Dia,
    "dia-feira": _diafeira,
    "D": _D,
}


def map_to_strf(texto):
    for key, val in MAPA_DATAHORA.items():
        if key in texto:
            texto = texto.replace(key, val)
    return texto

def formato(datetime, fmt="%x"): 
    strfmt = map_to_strf(fmt)
    for key, func in MAPA_DATAHORA_EXTRA.items():
        if key in strfmt:
            strfmt = strfmt.replace(key, func(datetime))
    return datetime.strftime(strfmt)

def teste1():
    texto1 = "ds, DD de mmm de AAAA"
    saida1 = map_to_strf(texto1)
    assert saida1 == "%a, %d de %b de %Y"

if __name__ == '__main__':
    texto = "Dia, DD de mês de AAAA (HHhmm)"
    fmt = map_to_strf(texto)
    print(fmt)
    print(formato(datetime.now(),fmt))
    teste1()