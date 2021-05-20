import jinja2
import os
from jinja2 import Template
from datetime import date
from pathlib import Path

def data(datetime, formato="%d/%m/%Y"): 
    return datetime.strftime(formato)

EXTRA_FUNCTIONS = {"data": data } 

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
    #for key, value in EXTRA_FUNCTIONS.items():
    #    latex_jinja_env.globals[key] = value
    #print(caminhos)
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
        output = full_caminho.parent / ("compilado_" + full_caminho.name)
    
    renderizado = render_template(filename, dicionario)

    with open(output, "w") as fp:
        fp.write(renderizado)  

