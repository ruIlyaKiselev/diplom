import csv

from processed_question import ProcessedQuestion
from question_from_site import QuestionFromSite


class CsvUtils:

    @staticmethod
    def save_question_from_site(items, path):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            for item in items:
                writer.writerow([
                    item['id'].replace(';', ' '),
                    item['title'].replace(';', ''),
                    item['question'].replace(';', ''),
                    item['link'].replace(';', ''),
                    item['createdAt'].replace(';', ''),
                    item['updatedAt'].replace(';', ''),
                    item['posts'].replace(';', ''),
                    item['views'].replace(';', ''),
                    item['answers'].replace(';', '')
                ])

    @staticmethod
    def load_question_from_site(path):
        result = []
        with open(path, newline='') as file:
            reader = csv.reader(file, delimiter=';')
            data = [tuple(row) for row in reader]
            for item in data:
                result.append(
                    QuestionFromSite(
                        item[0],
                        item[1],
                        item[2],
                        item[4],
                        item[5],
                        item[8],
                    )
                )
            return result

    @staticmethod
    def save_processed_question(processed_questions, path):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            for item in processed_questions:
                writer.writerow(
                    [item.question_id] +
                    item.categories_list
                )

    @staticmethod
    def load_processed_question(path):
        result = []
        with open(path, newline='') as file:
            reader = csv.reader(file, delimiter=';')
            data = [tuple(row) for row in reader]
            for item in data:
                result.append(
                    ProcessedQuestion(
                        item[0],
                        item[1:]
                    )
                )
            return result
