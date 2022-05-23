from yargy.tokenizer import MorphTokenizer
import re
from math import *


class CompositeToken:

    def add_form(self, form):
        self.forms.add(form)

    def increment_count(self):
        self.count += 1

    def __init__(self, lemma):
        self.lemma = lemma
        self.forms = set()
        self.count = 1

    def __eq__(self, other):
        return self.lemma == other.lemma

    def __repr__(self):
        return self.lemma + " " + self.forms.__str__() + " " + self.count.__str__()

    def __hash__(self):
        return hash(self.lemma)


class TokenizedSentence:

    def __init__(self):
        self.tokens = list()
        self.words_count = 0

    def add_token(self, lemma):
        self.words_count += 1
        token_index = self.search(lemma)
        if token_index == -1:
            self.tokens.append(
                CompositeToken(
                    lemma
                )
            )
        else:
            self.tokens[token_index].increment_count()

    def add_form(self, lemma, form):
        token_index = self.search(lemma)
        self.tokens[token_index].add_form(form)

    def search(self, lemma):
        for i in range(len(self.tokens)):
            if self.tokens[i].lemma == lemma:
                return i
        return -1

    def __repr__(self):
        return self.tokens.__str__()


class TokensSplitter:
    @staticmethod
    def split_corpus_string_to_tokens(
            input_string,
            unique_words,
            word_appear_map
    ):
        string_without_symbols = ParserUtils.remove_irrelevant_symbols(input_string)
        # print(string_without_symbols)
        tokenizer = MorphTokenizer()
        tokens = TokenizedSentence()
        morph_tokens = list(tokenizer(string_without_symbols))
        for token in morph_tokens:

            tokens.add_token(
                token.normalized
            )

            unique_words.add_token(
                token.normalized
            )

            if token.normalized in word_appear_map:
                word_appear_map[token.normalized] += 1
            else:
                word_appear_map[token.normalized] = 1

            if token.type == "RU":
                for form in token.forms:
                    tokens.add_form(
                        form.normalized,
                        form.raw.tag.POS
                    )
                    unique_words.add_form(
                        form.normalized,
                        form.raw.tag.POS
                    )

        return tokens

    @staticmethod
    def split_input_string_to_tokens(input_string):
        string_without_symbols = ParserUtils.remove_irrelevant_symbols(input_string)
        tokenizer = MorphTokenizer()
        tokens = TokenizedSentence()
        morph_tokens = list(tokenizer(string_without_symbols))
        for token in morph_tokens:

            tokens.add_token(
                token.normalized
            )

            if token.type == "RU":
                for form in token.forms:
                    tokens.add_form(
                        form.normalized,
                        form.raw.tag.POS
                    )

        return tokens


class TfIdfVectorizer:

    @staticmethod
    def vectorize_corpus_tokenized_sentence(
            current_tokenized_sentence,
            unique_words,
            idf_map
    ):
        current_vectorized_sentence_accumulator = []
        for current_unique_word in unique_words.tokens:
            if current_unique_word in current_tokenized_sentence.tokens:
                current_token_index = current_tokenized_sentence.tokens.index(current_unique_word)
                current_token = current_tokenized_sentence.tokens[current_token_index]
                tf = (current_token.count / current_tokenized_sentence.words_count)
                current_vectorized_sentence_accumulator.append(tf * idf_map[current_token.lemma])
            else:
                current_vectorized_sentence_accumulator.append(0)

        return current_vectorized_sentence_accumulator

    @staticmethod
    def vectorize_input_tokenized_sentence(
            current_tokenized_sentence,
            unique_words,
            idf_map,
            word_appear_map
    ):
        current_vectorized_sentence_accumulator = []
        for current_unique_word in unique_words.tokens:
            if current_unique_word in current_tokenized_sentence.tokens:
                current_token_index = current_tokenized_sentence.tokens.index(current_unique_word)
                current_token = current_tokenized_sentence.tokens[current_token_index]
                tf = (current_token.count / word_appear_map[current_token.lemma])
                current_vectorized_sentence_accumulator.append(tf * idf_map[current_token.lemma])
            else:
                current_vectorized_sentence_accumulator.append(0)

        return current_vectorized_sentence_accumulator


class ParserUtils:

    @staticmethod
    def remove_irrelevant_symbols(raw_string):
        symbol_regex = re.compile('[-_,.;:"\'!?()[]')
        return symbol_regex.sub(' ', raw_string)
