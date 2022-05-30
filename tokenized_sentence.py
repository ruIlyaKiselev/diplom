from composite_token import CompositeToken


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
