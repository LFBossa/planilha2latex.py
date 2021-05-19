# planilha2latex.py
Crie um template em LaTeX, alimente com dados vindos de uma planilha e compile. 

## Instalação

* Tenha o `pipenv` instalado na sua máquina
* Dentro desse diretório, rode o comando `pipenv install` para instalar as dependências

## Rodando o exemplo 
* Para compilar o exemplo, rode o comando `pipenv run python compilar_exemplo.py`
* O arquivo compilado vai estar no diretório raiz, em `output_exemplo.tex`.

## Templates dentro do `LaTeX`

Basicamente o que foi feito, conforme as referências, foi uma pequena modificação 
nos templates do Jinja2. Para executar um comando Python em tempo de compilação, 
basta iniciar uma linha com `%>>>`. Para expandir o valor de uma variável `x`, usa-se
o comando `\VAR{x}`. 