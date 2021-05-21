import click
from pathlib import Path
from ferramentas.planilha import planilha2dicionario
from ferramentas.latex import processa_template



@click.command(help="""TEMPLATE é o arquivo .tex principal a ser processado.\n
PLANILHA é a planilha da qual são extraídos os dados.""")
@click.argument("template", type=click.Path(), required=True)
@click.argument("planilha", type=click.Path(), required=True)
def main(template, planilha): 
    dados = planilha2dicionario(planilha)
    processa_template(template, dados)


if __name__ == "__main__":
    main()