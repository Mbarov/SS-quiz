from .dto import ChoiceDTO, QuestionDTO, QuizDTO, AnswerDTO, AnswersDTO
from typing import List


class QuizResultService():
    def __init__(self, quiz_dto: QuizDTO, answers_dto: AnswersDTO):
        self.quiz_dto = quiz_dto
        self.answers_dto = answers_dto

    def get_result(self) -> float:
        score = 0
        correct_answer_quiz = 0
        all_answers = self.answers_dto.objects.get(quiz_uuid=1).answers.all()#переделать
        for answer in all_answers:
            for choice in answer.choices.all():
                if choice.is_correct:
                    score += 1
        quiz_object = self.quiz_dto.objects.get(uuid=1)
        questions = quiz_object.questions.all()
        for question in questions:
            correct_answer_quiz += question.choices.filter(is_correct=True).count()
        result = round((score / correct_answer_quiz), 2)
        return result


