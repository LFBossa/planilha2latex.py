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

_Ds =  lambda x: x.strftime("%a").capitalize()
_Dia = lambda x: x.strftime("%A").capitalize()
_Diafeira = lambda x: _Dia(x)+"-feira" if x.weekday() < 5 else _Dia(x)
_diafeira = lambda x: _Diafeira(x).lower()

MAPA_DATAHORA_EXTRA = {
    "Ds": _Ds,
    "Dia-feira": _Diafeira, 
    "Dia": _Dia,
    "dia-feira": _diafeira
}


def map_to_strf(texto):
    for key, val in MAPA_DATAHORA.items():
        texto = texto.replace(key, val)
    return texto

def data(datetime, fmt="%d/%m/%Y"): 
    return datetime.strftime(fmt)

def teste1():
    texto1 = "ds, DD de mmm de AAAA"
    saida1 = map_to_strf(texto1)
    assert saida1 == "%a, %d de %b de %Y"

if __name__ == '__main__':
    texto = "ds, DD de mmm de AAAA"
    formato = map_to_strf(texto)
    print(formato)
    print(data(date.today(),formato))
    teste1()