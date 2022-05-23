from parser import TokensSplitter
from scrapper import parse_pages, parse_details
from traffic_rules_corpus import TrafficRulesCorpus
from scipy import spatial


def main():
    # parse_pages()
    #parse_details('https://pddclub.ru/kommentarii-k-pravila-buksirovki-pricepa-v-2022-godu-t4939.html')
    corpus = TrafficRulesCorpus()
    print(corpus.unique_words.tokens)
    print(len(corpus.unique_words.tokens))
    print(corpus.word_appear_map)
    print(corpus.corpus_vectors["15.2."][-1])
    print(corpus.compare_sentence("При повороте налево или развороте по зеленому сигналу светофора водитель безрельсового транспортного средства обязан уступить дорогу транспортным средствам, движущимся со встречного направления прямо или направо. Таким же правилом должны руководствоваться между собой водители трамваев."))

main()
