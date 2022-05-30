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
