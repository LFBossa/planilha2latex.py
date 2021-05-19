import jinja2
import os
from jinja2 import Template
from datetime import date


def data(numero, formato="%d/%m/%Y"):
    data = date.fromtimestamp(numero)
    return data.strftime(formato)


latex_jinja_env = jinja2.Environment(
    block_start_string = '\BLOCK{',
    block_end_string = '}',
    variable_start_string = '\VAR{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%>>>',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader([os.path.abspath('.'), os.path.abspath('./exemplos')]),
)

latex_jinja_env.globals["data"] =  data


def render_template(filename, dicionario):
    """Lê um template .tex e retorna uma string, passando dicionário como dados."""
    template = latex_jinja_env.get_template(filename)
    return template.render(dicionario)


def processa_template(filename, dicionario, output = None):
    """Abre um template, preenche com os dados de dicionario e salva no arquivo output"""
    if not output:
        output = "compilado_" + filename
    
    renderizado = render_template(filename, dicionario)

    with open(output, "w") as fp:
        fp.write(renderizado)  
