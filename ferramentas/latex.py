import jinja2
import os
from jinja2 import Template
from datetime import date
from pathlib import Path
import locale
locale.setlocale(locale.LC_TIME, "pt_BR.utf8")

from .filtros import formato, lista_tags, tags_unicas

EXTRA_FUNCTIONS = { } 

def create_environment(template_path):
    template_dir = Path(template_path).parent.absolute()
    caminhos1 = [ template_dir ]
    caminhos = [ x.as_posix() for x in caminhos1]
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
        loader = jinja2.FileSystemLoader(caminhos),
    )
    FILTROS = {"formato": formato, "lista_tags": lista_tags, "tags_unicas": tags_unicas }
    for key, val in FILTROS.items():
        latex_jinja_env.filters[key] = val
    
    return latex_jinja_env


def render_template(filename, dicionario):
    """Lê um template .tex e retorna uma string, passando dicionário como dados."""
    full_path = Path(filename)

    latex_jinja_env = create_environment(filename)
    ## o get_template fica sempre relativo :(
    template = latex_jinja_env.get_template(full_path.name, globals=EXTRA_FUNCTIONS)
    return template.render(dicionario)


def processa_template(filename, dicionario, output = None):
    """Abre um template, preenche com os dados de dicionario e salva no arquivo output"""
    if not output:
        full_caminho = Path(filename)
        novo_nome = full_caminho.stem + "_compilado" + full_caminho.suffix
        output = full_caminho.parent / novo_nome
    
    renderizado = render_template(filename, dicionario)

    with open(output, "w") as fp:
        fp.write(renderizado)  

