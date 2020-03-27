import json
from argparse import ArgumentParser
from nltk.tokenize import word_tokenize
from nltk.tokenize import sexpr_tokenize
import re

def busca(index, repo, corpus, word):
    # Parsing da query.
    # "banana apple" => "banana" and "apple"
    # Recuperar os ids de documento que contem todos os termos da query.
    # words = word_tokenize(query)
    # words = ["the", ]
    print(words)
    
    docids_list = []
    
    # for word in words:
    try:
        docids = index[word] 
        docids_list.append(set(docids))

    except:
        print("Nao exite(m) essa(s) palavra(s) no corpus")
        # break
    
    res = docids_list[0]
    # TODO adicionar para OR tambem
    for docid in docids_list:
        res &= docid
    return res

    # (banana apple) grape => (banana OR apple) AND grape
    
    # Retornar os textos destes documentos.
    # return [corpus[docid] for docid in docids]

def buscaid(index, word):
    try:
        docids = index[word] 
        return set(docids)
        # docids_list.append(set(docids))

    except:
        print("Nao exite(m) essa(s) palavra(s) no corpus")
        # break
    
    

def teste2(index, texto):
    if not(' ') in texto:
        if not('(') in texto:
            if texto == "and" or texto == "or":
                return texto
            return buscaid(index, texto)
    
    a = sexpr_tokenize(texto)
    if len(a)==1:
        a = a[0].split()
    # result = True
    pilha = []
    for e in a:
        e = re.sub('\)$', '', e)
        e = re.sub('^\(', '', e)
        pilha.append(teste2(index, e))

    result = [pilha[0]]
    for i, word in enumerate(pilha):
        if word == 'and':
            result[0] &= pilha[i+1]
        if word == 'or':
            result[0] |= pilha[i+1]
    return result[0]

def main():
    parser = ArgumentParser()
    parser.add_argument('corpus', help='Arquivo do corpus.')
    parser.add_argument('repo', help='Arquivo do repo.')
    parser.add_argument('index', help='Arquivo do index.')
    
    parser.add_argument('query', help='A query (entre aspas)')
    args = parser.parse_args()

    with open(args.repo, 'r') as file:
        repo = json.load(file)

    with open(args.index, 'r') as file:
        index = json.load(file)

    with open(args.corpus, 'r') as file:
        corpus = json.load(file)
    
    print(teste2(index, args.query))


if __name__ == '__main__':
    main()
