from datetime import date, time, datetime
import locale
from os import posix_fadvise 
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

def tags_unicas(lista):
    """Retorna um dicionário no formato {n: string} com as ocorrências únicas 
    das strings na lista. """
    i = 1
    dicio = dict()
    for val in lista:
        if val not in dicio:
            dicio[val] = i
            i = i + 1
    return dicio

def lista_tags(lista):  
    """Retorna uma lista de pares ordenados (tag, string) para cada string em lista."""
    dicionario = tags_unicas(lista)
    return [(v,dicionario[v]) for v in lista]

def teste1():
    texto1 = "ds, DD de mmm de AAAA"
    saida1 = map_to_strf(texto1)
    assert saida1 == "%a, %d de %b de %Y"

def processa_lista(lista, formato):
    """Recebe uma lista e coloca dentro de uma string de formato. 
        - @A representa o primeiro item da lista 
        - @Z representa o ultimo item da lista 
        - @X  @Y representam itens genéricos da lista, e o conteúdo entre eles
        será repetido como ligação entre os itens da lista.
        
        Exemplo: 
        lista = ['1', 'B', 'C', 'D', 'E']
        fmt = "(@A): @X, @Y & @Z"
        processa_lista(lista, fmt) -> "(1): B, C, D & E"
        """
    #iVAR -> indice Variavel
    #cVAR -> conteudo 
    dados = lista.copy()
    iA = formato.find("@A")
    iZ = formato.find("@Z")
    if iA >= 0:
        cA = dados.pop(0)
        formato = formato.replace("@A", cA)
    if iZ >= 0:
        cZ = dados.pop(-1)
        formato = formato.replace("@Z", cZ)

    iX = formato.find("@X")
    iY = formato.find("@Y")
    ligante = formato[iX+2:iY]  # tudo o que estiver entre @X e @Y
    texto = ligante.join(dados) # vai ser repetido ligando os termos da lista
    completo = formato[:iX] + texto + formato[iY+2:]
    return completo

def latexfy(string):
    try:
        return string.replace("_", "\\_").replace("&", "\&")
    except:
        return string

if __name__ == '__main__':
    texto = "Dia, DD de mês de AAAA (HHhmm)"
    fmt = map_to_strf(texto)
    print(fmt)
    print(formato(datetime.now(),fmt))
    teste1()
    print(lista_tags(["Luiz", "Fernando", "Bossa", "Bossa"]))
    print(processa_lista("A,B,C,D,E".split(","), "(@A): @X, @Y & @Z"))