import json
from argparse import ArgumentParser
from nltk.tokenize import word_tokenize
from nltk.tokenize import sexpr_tokenize
import re
from nltk.text import TextCollection
from nltk.corpus import reuters
from collections import Counter


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
'''     
https://norvig.com/spell-correct.html
'''

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read())) #### o que é esse big?????

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
     ------------------ 
'''

def spell_check(word):
    c = correction(word)
    if c:
        return 'tente buscar por:' + c
    else:
        return ''

def buscaid(index, word):
    try:
        docids = index[word] 
        return set(docids)
        # docids_list.append(set(docids))

    except:
        res = spell_check(word)
        raise Exception(f"Nao exite a palavra \'{word}\' no index, , {res}")
    

palavras = []
def teste2(index, texto, pilha=[]):
    if not(' ') in texto:
        if not('(') in texto:
            if texto == "and" or texto == "or":
                return texto
            palavras.append(texto)
            return buscaid(index, texto)
    
    a = sexpr_tokenize(texto)
    if len(a)==1:
        a = a[0].split()
    # result = True
    
    for e in a:
        e = re.sub('\)$', '', e)
        e = re.sub('^\(', '', e)
        pilha.append(teste2(index, e, pilha))

    result = [pilha[0]]
    
    for i, word in enumerate(pilha):
        if word == 'and':
            result[0] &= pilha[i+1]
        if word == 'or':
            result[0] |= pilha[i+1]
    return result[0], palavras

def ranking(corpus, corpus_mod, docids, palavras):
# , repo, index, docids, palavras):
    # Ranquear os documentos.
    return(docids)
    print(docids, palavras)
    rank = {}
    
    for e in docids:
        rank[e]=0
        for i in palavras:
            # print(corpus[e])
            # print()
            rank[e]+=TextCollection(corpus).tf_idf(i, corpus_mod[e])
    rank = {k: v for k, v in reversed(sorted(rank.items(), key=lambda item: item[1]))}
    return rank.keys()
    # return list(docids)  # dummy por enquanto.

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
    
    docids, palavras = teste2(index, args.query)
    print(ranking(reuters, corpus, docids, palavras))
    # print(TextCollection(reuters).idf("the"))
    # print([i.idf('asian') for i in TextCollection(reuters)])

if __name__ == '__main__':
    main()
