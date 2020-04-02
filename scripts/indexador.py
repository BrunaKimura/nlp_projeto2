import json
from argparse import ArgumentParser
from collections import defaultdict

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def create_repo(corpus):
    '''Cria o repositorio.

    Args:
        corpus: dicionario que mapeia um docid para uma string contendo o
                documento completo.

    Returns:
        Um dicionário que mapeia docid para uma lista de tokens.
    '''
    # TODO melhorar tokenizer (tirar stopwords, ver mais coisas)
    sw = stopwords.words('english')+['.', ',', '\'s', '(', ')', 'n\'t', '``', ';', ':']
    print(sw)
    # {docid: word_tokenize(text) for docid, text in corpus.items()}
    doc_ids={}
    for docid, text in corpus.items():
        doc_ids[docid]=[]
        for word in word_tokenize(text):
            
            if word.lower() not in sw:
                if word.lower() not in doc_ids[docid]:
                    doc_ids[docid].append(word.lower())

    return doc_ids
    # return {((docid: word_tokenize(text) )if (word_tokenize(text) not in sw)) for docid, text in corpus.items()}


def create_index(repo):
    '''Indexa os documentos de um corpus.

    Args:
        repo: dicionario que mapeia docid para uma lista de tokens.

    Returns:
        O índice reverso do repositorio: um dicionario que mapeia token para
        lista de docids.
    '''
    
    indexed = defaultdict(set)
    for doc_id, words in repo.items():
        for word in words:
            indexed[word].add(doc_id)

    return {word: list(doc_ids) for word, doc_ids in indexed.items()}


def main():
    parser = ArgumentParser()
    parser.add_argument('corpus',
                        help='Arquivo json com um dicionario docid para texto')
    parser.add_argument('repo_name',
                        help='Raiz do nome do arquivo de repositorio')
    args = parser.parse_args()

    with open(args.corpus, 'r') as file_corpus:
        corpus = json.load(file_corpus)

    repo = create_repo(corpus)
    index = create_index(repo)

    with open(args.repo_name + '_repo.json', 'w') as file_repo:
        json.dump(repo, file_repo, indent=4)

    with open(args.repo_name + '_index.json', 'w') as file_index:
        json.dump(index, file_index, indent=4)


if __name__ == '__main__':
    main()
