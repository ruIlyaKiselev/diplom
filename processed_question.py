class ProcessedQuestion:
    def __init__(self, question_id, categories_list):
        self.question_id = question_id
        self.categories_list = categories_list

    def __eq__(self, other):
        return self.question_id == other.question_id

    def __repr__(self):
        return self.question_id.__str__() + " " + self.categories_list.__str__()

    def __hash__(self):
        return hash(self.question_id)
