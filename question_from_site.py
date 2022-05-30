class QuestionFromSite:
    def __init__(self, question_id, title, question, created_at, last_update, answers_list):
        self.question_id = question_id
        self.title = title
        self.question = question
        self.created_at = created_at
        self.last_update = last_update
        self.answers_list = answers_list

    def __eq__(self, other):
        return self.title == other.title and self.question == other.question

    def __repr__(self):
        return self.question_id.__str__() + "\n" + \
               self.title.__str__() + "\n" + \
               self.question.__str__() + "\n" + \
               self.created_at.__str__() + "\n" + \
               self.last_update.__str__() + "\n" + \
               self.answers_list.__str__()

    def __hash__(self):
        return hash(self.title) + hash(self.question)
