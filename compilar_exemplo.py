from ferramentas.planilha import planilha2dicionario
from ferramentas.latex import processa_template


if __name__ == '__main__':
    filename = "exemplos/exemplo.tex"
    dados = planilha2dicionario("exemplos/planilha_exemplo.xlsx")
    processa_template(filename, dados, "output_exemplo.tex")