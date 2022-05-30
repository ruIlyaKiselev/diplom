import re


class ParserUtils:

    @staticmethod
    def remove_irrelevant_symbols(raw_string):
        symbol_regex = re.compile('[-_,.;:"\'!?()[]')
        return symbol_regex.sub(' ', raw_string)
