import json
from argparse import ArgumentParser
from nltk.tokenize import word_tokenize


def busca(index, repo, corpus, query):
    # Parsing da query.
    # "banana apple" => "banana" and "apple"
    # Recuperar os ids de documento que contem todos os termos da query.
    words = word_tokenize(query)
    # words = ["the", ]
    print(words)
    
    docids_list = []
    
    for word in words:
        try:
            docids = index[word] 
            docids_list.append(set(docids))

        except:
            print("Nao exite(m) essa(s) palavra(s) no corpus")
            break
    
    res = docids_list[0]
    # TODO adicionar para OR tambem
    for docid in docids_list:
        res &= docid
    return res

    # (banana apple) grape => (banana OR apple) AND grape
    
    # Retornar os textos destes documentos.
    # return [corpus[docid] for docid in docids]


def main():
    parser = ArgumentParser()
    parser.add_argument('repo', help='Arquivo do repo.')
    parser.add_argument('index', help='Arquivo do index.')
    parser.add_argument('corpus', help='Arquivo do corpus.')
    parser.add_argument('query', help='A query (entre aspas)')
    args = parser.parse_args()

    with open(args.repo, 'r') as file:
        repo = json.load(file)

    with open(args.index, 'r') as file:
        index = json.load(file)

    with open(args.corpus, 'r') as file:
        corpus = json.load(file)
    
    print(busca(index, repo, corpus, args.query))


if __name__ == '__main__':
    main()
