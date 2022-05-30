from yargy.tokenizer import MorphTokenizer

from parse_utils import ParserUtils
from tokenized_sentence import TokenizedSentence


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
