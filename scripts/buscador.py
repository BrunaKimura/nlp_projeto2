import json
from argparse import ArgumentParser
from nltk.tokenize import word_tokenize
from nltk.tokenize import sexpr_tokenize
import re
from nltk.text import TextCollection
from nltk.corpus import reuters
from collections import Counter

'''     
https://norvig.com/spell-correct.html
'''

def words(text): return re.findall(r'\w+', text.lower())

with open('corpus_reuters.json', 'r') as file:
    corpus = json.load(file)
big = ''
for v in corpus.values():
    big += v

WORDS = Counter(words(big))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

'''
------------------------------------------- 
'''

def spell_check(word):
    '''Checa erros na escrita de uma palavra

    Args:
        word: palavra a ser buscada
    
    Returns:
        Possivel palavra depois de correção
    '''
    c = correction(word)
    return 'tente buscar por:' + c

def buscaid(index, word):
    '''Busca os índices dos documentos onde a palavra (word) aparece

    Args:
        index: dicionário que associa cada palavra do corpus com os documentos 
               em que ela aparece
        word: palavraa ser buscada
    
    Returns:
        Dicionario com os docids que possuem a palavra, caso não exista a palavra, 
        retorna uma mensagem contendo uma sugestão de busca
    '''
    try:
        docids = index[word] 
        return set(docids)
    except:
        res = spell_check(word)
        raise Exception(f"Nao exite a palavra \'{word}\' no index, tente buscar por {res}")
    

def busca(index, texto, pilha=[]):
    '''Busca os textos de acordo com a query

    Args:
        index: dicionário que associa cada palavra do corpus com os documentos em que ela aparece
        texto: query de busca
        pilha: contém os índices buscados
    
    Returns:
        Lista com os índices correspondentes a query
    '''
    if not(' ') in texto:
        if not('(') in texto:
            if texto == "and" or texto == "or":
                return texto
            return buscaid(index, texto)
    
    a = sexpr_tokenize(texto)
    if len(a)==1:
        a = a[0].split()

    for e in a:
        e = re.sub('\)$', '', e)
        e = re.sub('^\(', '', e)
        pilha.append(busca(index, e, pilha))

    result = [pilha[0]]
    
    for i, word in enumerate(pilha):
        if word == 'and':
            result[0] &= pilha[i+1]
        if word == 'or':
            result[0] |= pilha[i+1]
    return result[0]

def ranking(reuters, corpus, docids, palavras):
    '''Cria um ranqueamento entre os textos da busca, sendo o primeiro o mais relevante

    Args:
        reuters: corpus vindo do nltk
        corpus: dicionário contendo a relação entre índice e texto
        docids: índices dos textos buscados
        palavras: palavras tokenizadas da query
    
    Returns:
        Lista com todas os índices já ranqueados
    '''
    rank = {}
    tc = TextCollection(reuters)

    for e in docids:
        rank[e]=0
        for i in palavras:
            rank[e]+=tc.tf_idf(i, corpus[e])

    rank = {k: v for k, v in reversed(sorted(rank.items(), key=lambda item: item[1]))}
    return rank.keys()


def tokens_palavras(texto):
    '''Tokeniza o texto da query

    Args:
        texto: texto da query
    
    Returns:
        Lista com todas as palavras da query sem as palavras reservadas
    '''
    palavras = []
    for word in word_tokenize(texto):
        if not (word == "(" or word == ")" or word == "and" or word == "or"):
            palavras.append(word)
    return palavras

def docid_to_text(docids, corpus):
    '''Mostra texto(s) correspondentes aos docids.

    Args:
        docids: contém todos os índices correspondentes à busca
        corpus: dicionario que mapeia um docid para uma string contendo o
                documento completo.
    '''
    for docid in docids:
        print(f'docid: {docid}')
        print(f'{corpus[docid]}' )
        print('-------------------------------------------------------------')

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
    
    docids = busca(index, args.query)
    palavras = tokens_palavras(args.query)
    docid_to_text(ranking(reuters, corpus, docids, palavras), corpus)


if __name__ == '__main__':
    main()
