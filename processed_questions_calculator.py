class ProcessedQuestionsCalculator:

    @staticmethod
    def find_top_categories(processed_questions, top_limit):
        top_categories = {}

        for processed_question in processed_questions:
            for category in processed_question.categories_list:
                start1 = category.find('(\'') + 2
                finish1 = category.find('\',')
                start2 = category.find(', ') + 2
                finish2 = category.find(')')
                category_name = category[start1:  finish1]
                category_value = float(category[start2:  finish2])
                if category_name in top_categories:
                    top_categories[category_name] += category_value
                else:
                    top_categories[category_name] = category_value

        return sorted(top_categories.items(), key=lambda kv: kv[1], reverse=True)[0:top_limit]

    @staticmethod
    def questions_by_top_categories(questions_from_site, processed_questions, top_categories):
        ids_with_categories = {}
        questions_with_categories = {}

        for current_top_category in top_categories:
            ids_with_categories[current_top_category[0]] = []
            questions_with_categories[current_top_category[0]] = []

        for current_processed_question in processed_questions:
            start1 = current_processed_question.categories_list[0].find('(\'') + 2
            finish1 = current_processed_question.categories_list[0].find('\',')
            current_processed_question_category_value = current_processed_question.categories_list[0][start1:finish1]
            for current_top_category in top_categories:
                current_top_category_value = current_top_category[0]
                if current_processed_question_category_value == current_top_category_value:
                    ids_with_categories[current_top_category_value].append(current_processed_question.question_id)

        for key in ids_with_categories:
            current_values = ids_with_categories[key]
            for current_value in current_values:
                question_from_site = next(e for e in questions_from_site if e.question_id == current_value)
                questions_with_categories[key].append(question_from_site)

        return questions_with_categories

