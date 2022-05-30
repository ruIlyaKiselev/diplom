
from csv_utils import CsvUtils
from processed_questions_calculator import ProcessedQuestionsCalculator
from scrapper import parse_pages
from traffic_rules_corpus import TrafficRulesCorpus


def main(argv):

    for arg in argv:
        print(arg)

    # parse_pages(
    #     'https://pddclub.ru',
    #     '/voprosy-po-pdd-f15',
    #     '.html',
    #     "questions.csv"
    # )
    # corpus = TrafficRulesCorpus()
    #
    # processed_questions = []
    #
    # i = 1
    # for item in restored_questions:
    #     print(f'comparing question {i}/{restored_questions.__len__()}')
    #     processed_questions.append(corpus.compare_question_from_site(item))
    #     i += 1
    #
    # CsvUtils.save_processed_question(processed_questions, 'processed_questions.csv')

    questions = CsvUtils.load_question_from_site('questions.csv')
    processed_questions = CsvUtils.load_processed_question('processed_questions.csv')

    top_categories = ProcessedQuestionsCalculator.find_top_categories(processed_questions, 5)

    print(top_categories)

    top_questions = ProcessedQuestionsCalculator.questions_by_top_categories(
        questions,
        processed_questions,
        top_categories
    )

    print(top_questions)


main()
