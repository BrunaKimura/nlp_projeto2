# Projeto Máquina de busca
### Bruna Kimura e Elisa Malzoni
-------------------------------------------------------------------------


Neste projeto estamos desenvolvendo uma máquina de busca com as seguintes
características:

- queries booleanas;
- entendimento de query e auto-correção
- ranqueamento de resultados;

Fase 1: Construção do repositório e do índice.

Fase 2: Construção de uma ferramenta para busca com queries booleanas (AND, OR) e hierarquia (parênteses)

Fase 3: Ranking

Fase 4: Aperfeiçoamentos e melhoramento do ranking

## Gerando o corpus

O primeiro passo é gerar o *corpus*. Este documento possui todos os textos com um índice associado.

`$ python3 scripts/gera_corpus_reuters.py <corpus>`

`$ python3 scripts/gera_corpus_reuters.py corpus_reuters.json`

## Repositório e Índice

Para o funcionamento do buscador, é necessário dois documentos um para o repositório e o outro para os índices. O repositório é um dicionário que associa o índice à cada palavra existente naquele texto. Já o índice associa cada palavra à todos os documentos em que ela aparece.

`$ python3 scripts/indexador.py <corpus> <nome repo e indice>`

`$ python3 scripts/indexador.py corpus_reuters.json reuters`

## Buscador
 O buscador é separado em três parte: entender a query booleana e a hierarquia, correção de termos se necessário e ranqueamento dos textos.

`$ python3 scripts/buscador.py <corpus> <repo> <index> <query entre aspas>`

`$ python3 scripts/buscador.py corpus_reuters.json reuters_repo.json reuters_index.json 'last or (green or blue) and asia'`
