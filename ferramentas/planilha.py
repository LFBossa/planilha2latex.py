#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criado em 18 de maio de 2021

@author: LFBossa
"""

import openpyxl as pyxl
import pandas as pd
import json
import datetime as dt


# Funções auxiliares para tratar os dados conforme o tipo
def converte_data(timestamp):
    if isinstance(timestamp, pd.Timestamp):
        return timestamp.to_pydatetime()
    else:
        epoch = timestamp/1e3 if timestamp > 1e9 else timestamp
        return dt.datetime.fromtimestamp(epoch)


def converte_lista(string_lista):
    return string_lista.split(",")


def converte_hora(string_hora):
    if isinstance(string_hora, dt.time):
        return string_hora
    else:
        inteiros = [int(x) for x in string_hora.split(":")]
        return time(*inteiros)


def converte_numero(numero):
    return float(numero)


# mapeia o tipo do dado com a conversão necessária
MAPEAMENTO = {"data": converte_data,
              "hora": converte_hora,
              "numero": converte_numero,
              "lista": converte_lista}


def planilha2pandas(filename):
    """ Abre uma planilha e detorna um dicionário de DataFrames. 
    """
    planilha = pyxl.load_workbook(filename=filename)
    # carregamos o arquivo para pegar o nome das folhas

    banco_de_dados = {}

    for folha in planilha.sheetnames:
        # cada folha vira um DataFrame
        df = pd.read_excel(filename, sheet_name=folha, engine="openpyxl")
        colunas_remover = [x for x in df.columns if 'Unnamed' in x]
        # cada coluna que se chama Unnamed blablabla
        df.drop(labels=colunas_remover, axis=1, inplace=True)
        #                          é removida
        # agora vamos remover as linhas que são nulas
        df_notnull = df[~(df.isnull()).apply(min, axis=1)]
        # salvamos no dicionário
        banco_de_dados[folha] = df.copy()

    return banco_de_dados    

def process_df(df):
    """Recebe um DataFrame cujas colunas tem type hints e converte para o tipo adequado."""
    # vamos tratar cada coluna conforme o tipo dela
    for x in df.columns:
        colunas_excluir = []
        if ":" in x:
            colunas_excluir.append(x)
            nome, tipo = x.split(":")
            pos = df.columns.get_loc(x)
            new_serie = df[x].apply(MAPEAMENTO[tipo])
            df.insert(pos, nome, new_serie)
        df.drop(labels=colunas_excluir, axis="columns", inplace=True)

    return df

def preprocess_pandas_dict(pandas_dict):
    new_dict = {}
    for key, value in pandas_dict.items():
        newdf = process_df(value)
        new_dict[key] = newdf.to_dict(orient="records")
    return new_dict



def planilha2dicionario(filename):
    """ Abre uma planilha e detorna um dicionário com seu conteúdo. 
    """
    dicionario = planilha2pandas(filename)
    return preprocess_pandas_dict(dicionario)


if __name__ == '__main__':
    dicio = planilha2pandas("exemplos/planilha_exemplo.xlsx")
    df = dicio["Apresentacoes"]
    print(df.head(1).applymap(type).to_dict())
    print(planilha2dicionario("exemplos/planilha_exemplo.xlsx"))