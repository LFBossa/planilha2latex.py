#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criado em 18 de maio de 2021

@author: LFBossa
"""

import openpyxl as pyxl
import pandas as pd
import json

def planilha2dicionario(filename):
    """ Abre uma planilha e detorna um dicionário com seu conteúdo. 
    """
    planilha = pyxl.load_workbook(filename= filename)
    # carregamos o arquivo para pegar o nome das folhas

    banco_de_dados = {}

    for folha in planilha.sheetnames:
        # cada folha vira um DataFrame
        df = pd.read_excel(filename, sheet_name=folha, engine="openpyxl")
        colunas_remover = [ x for x in df.columns if 'Unnamed' in x ]
        # cada coluna que se chama Unnamed blablabla
        df.drop(labels=colunas_remover, axis=1, inplace=True)
        #                          é removida 
        # agora vamos remover as linhas que são nulas
        df_notnull = df[~(df.isnull()).apply(min, axis=1)]
        
        df_as_json = json.loads(df_notnull.to_json(orient="records") )
        # salvamos como um json
        banco_de_dados[folha] = df_as_json

    return banco_de_dados