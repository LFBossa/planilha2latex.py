# planilha2latex.py
Crie um template em LaTeX, alimente com dados vindos de uma planilha e compile. 

## Instalação

* Tenha o [`pipenv`](https://pypi.org/project/pipenv/) instalado na sua máquina.
* Dentro desse diretório, rode o comando `pipenv install` para instalar as dependências.

## Rodando o exemplo 

Para compilar o exemplo, rode o script `compilar-exemplo.sh`. Se tudo der certo, o arquivo compilado vai estar em  `exemplos/exemplo_compilado.tex`.


## Templates `Jinja2` dentro do `LaTeX`

Basicamente o que foi feito, conforme as referências, foi uma pequena modificação 
nos templates do Jinja2. Para executar um comando Python em tempo de compilação, 
basta iniciar uma linha com `%>>>` ou escrevê-lo dentro de `\BLOCK{}`. 
Para expandir o valor de uma variável `x`, usa-se o comando `\VAR{x}`. 

## Estrutura dos dados

A planilha `exemplos/planilha_exemplo.xlsx` contém apenas uma folha, chamada `Apresentacoes`, cujo conteúdo é o seguinte:

|   Inteiro | Data:data           | Horario:hora   |   Flutuante:numero | Autores:lista       | Textao                      |
|----------:|:--------------------|:---------------|-------------------:|:--------------------|:----------------------------|
|        25 | 2021-08-25 00:00:00 | 10:00:00       |             102.55 | Bossa,Luiz,Fernando | Lorem ipsum dolor sit am... |
|       154 | 2021-08-26 00:00:00 | 14:00:00       |            1024.15 | Alice,Bob           | Nulla facilisi. Donec sc... |
|       104 | 2021-08-27 00:00:00 | 10:25:00       |              20.54 | Donald,Knuth        | Vestibulum consectetur, ... |
|        48 | 2021-08-28 00:00:00 | 22:15:00       |              52.01 | Paul,Erdos          | Duis mollis vel odio ac ... |

Note que eu uso o padrão `NomeDaColuna:tipo` para declarar o tipo de valor encontrado na coluna. As colunas que não possuem isso têm seu tipo inferido pelo próprio `pandas`. 

A função `planilha2dicionario` lê essa planilha e retorna um dicionário no qual as chaves são os nomes das folhas da planilha, e o conteúdo dentro de cada chave é uma lista contendo os dados de cada linha da planilha, no formado de registros do tipo `{coluna: valor}`, como abaixo. Note que os valores já estão convertidos para os tipos `python` apropriados.

```json
{
  "Apresentacoes": [
    {
      "Inteiro": 25,
      "Data": datetime.datetime(2021,8,25),
      "Horario": datetime.time(10, 0),
      "Flutuante": 102.55,
      "Autores": ["Bossa", "Luiz", "Fernando"],
      "Textao": " Lorem ipsum dolor sit am..."
    },
    [...]
```

## Iterando sobre os dados

Dentro do template `LaTeX`, podemos iterar sobre os valores do nosso banco de dados da 
seguinte maneira

```latex
 % iteramos sobre todos os registros
\BLOCK{ for registro in Apresentacoes }

\textbf{\VAR{registro.Autores[0]}}  % vai imprimir o primeiro autor

\par \VAR{registro.Textao} % vai imprimir o Textao

\BLOCK{ endfor } 
% fecha o bloco for
```

## Formato de data e hora

Para uma variável do tipo `data` ou do tipo `hora`, podemos aplicar um filtro para imprimir 
seu valor da maneira desejada. Por exemplo, se tivemos variável `x = datetime.datetime(2021,6,29)`, podemos aplicar o filtro `formato` para imprimir essa data por extenso
```latex
\VAR{ x | formato("Dia, DD  de mês de AAAA")}
```
resultando no valor impresso 
```latex
Terça, 29 de junho de 2021
```

### Tabela de conversão para data e hora

O filtro `formato` recebe chaves que serão substituidas pelos respectivos valores da data passada.

| Chave | Conversão | Exemplo | 
|:-----:| ----------| ------- | 
| DD | Dia do mês, dois dígitos com zeros à esquerda. | 01, 02, 03, ..., 31 |
| D | Dia do mês, numérico sem zeros à esquerda. | 1, 2 , 3, ... , 31 |
| MM | Mês, dois dígitos com zeros a esquerda. | 01, 02, ... , 12 |
| mmm | Mês, abreviado para três letras em minúsculo. | jan, fev, ..., dez |
| mês | Mês, completo com letras em minúsculo. |  janeiro, fevereiro, ..., dezembro |
| Mês | Mês, completo com inicial maiúscula. | Janeiro, Fevereiro, ..., Dezembro |
| AA | Ano, dois dígitos numéricos. | 99, 00, 01, ..., 21 |
| AAAA | Ano, quatro dígitos numéricos. | 1999, 2000,..., 2021 |
| ds | Dia da semana, três letras em minúsculo. | seg, ter, ..., dom |
| Ds | Dia da semana, três letras, inicial maiúscula. | Seg, Ter, ..., Dom |
| dia | Dia da semana, somente um nome em minúsculas. | segunda, terça, ..., domingo |
| Dia | Dia da semana, somente um nome, inicial maiúscula. | Segunda, Terça, ..., Domingo |
| dia-feira | Dia da semana, completo. | segunda-feira, ..., domingo |
| Dia-feira | Dia da semana, completo, inicial maiúscula. | Segunda-feira, ..., Domingo |
| HH | Hora, dois dígitos, formato 24h. | 00, 01, ..., 23 |
| mm | Minutos, dois dígitos. | 00, 01, ..., 59 | 


## Referências

* [Latex generator using Jinja](https://manu.hbrt.eu/latex-generator-using-jinja.html)
* [Combining LATEX with Python](https://tug.org/tug2019/slides/slides-ziegenhagen-python.pdf)
* [Latex with Jinja2](https://miller-blog.com/latex-with-jinja2/)

TODO

* [x] Converter a planilha em dicionário
* [x] Ler um arquivo LaTeX com tags e alimentar com dados do dicionário
* [x] Ferramenta de linha de comando para compilar templates
* [ ] Feramenta para compilar o tex gerado 
* [x] Filtros e funções extra para datas no Jinja Environment