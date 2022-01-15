from .dto import ChoiceDTO, QuestionDTO, QuizDTO, AnswerDTO, AnswersDTO
from typing import List


class QuizResultService():
    def __init__(self, quiz_dto: QuizDTO, answers_dto: AnswersDTO):
        self.quiz_dto = quiz_dto
        self.answers_dto = answers_dto

    def get_result(self) -> float:
        score = 0
        quiz_object = self.quiz_dto.objects.get(uuid=1)
        questions = quiz_object.questions.all()
        questions_count = questions.count()
        for question in questions:
            answers_list = []
            correct_choices_list = []
            
            for choice in question.choices.filter(is_correct=True):#выбор всех правильных вариантов ответа для выбранного вопроса
                correct_choices_list.append(choice.uuid)
            answer_list = self.answers_dto.objects.get(quiz_uuid=1).answers.all()#список всех ответов пользователя
            question_id = question.uuid
            user_choices = answer_list.get(question_id=question_id).choices.all()#список всех отмеченных вариантов на выбранный вопрос
            for user_choice in user_choices:
                answers_list.append(user_choice.uuid)
            if answers_list == correct_choices_list: #проверка соответствия ответа пользователя и правильных вариантов ответа на конкретный вопрос
                score += 1
        result = round((score / questions_count), 2)
        return result

