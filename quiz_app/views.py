from django.shortcuts import render
from .models import Quiz, Question, Answer, Answers, Choice
from django.core.exceptions import ObjectDoesNotExist
from quiz.services import QuizResultService

def main(request):
    try:#очистка старых ответов из БД 
        Answer.objects.all().delete()
        Answers.objects.all().delete()
    except:
        pass
    return render(request, 'quiz_app/main.html')

def save_user_answer(user_answer): 
    choice = Choice.objects.get(uuid=user_answer[0])
    question = Question.objects.get(choices__uuid=choice.uuid)#определяем uuid вопроса по выбранному ответу
    quiz = Quiz.objects.get(questions__uuid=question.uuid)#определяем uuid викторины по выбранному ответу
    try:#Проверка существования в БД ответа на вопрос(для возвращения на предыдущий вопрос и изменения ответа)
        answer = Answer.objects.get(question_id=question.uuid)
        answer.delete()
    except:
        pass
    answer = Answer.objects.create(question_id=str(question.uuid))#создание объекта модели Answer
    answer.save()
    for user_answer in user_answer:
        choice = Choice.objects.get(uuid=user_answer)
        answer.choices.add(choice)
    try:#Проверка существования экземпляра класса Answers
            all_answers = Answers.objects.get(quiz_uuid=quiz.uuid)        
    except ObjectDoesNotExist:#создание экземпляра класса Answers        
            all_answers = Answers.objects.create(quiz_uuid=quiz.uuid)
            all_answers.save()
    all_answers.answers.add(answer)    
    return all_answers


def questions(request, question):
    user_answer=(request.GET.getlist('abc[]'))
    if user_answer:#проверка получения ответа, и добавление ответа в БД
        save_user_answer(user_answer)     
    length = Question.objects.all().count()#Количество вопросов
    previous_number = int(question) - 1 #номер предыдущего вопроса
    if int(question) < length+1:
        question_object = Question.objects.get(uuid=question[-1])
        count_correct_choices = question_object.choices.filter(is_correct=True).count()#Подсчет количества правильных вариантов ответа в вопросе
        next_number = int(question) + 1 #номер следующего вопроса
        data = {'question_object':question_object, 'next_number': next_number, 'previous_number': previous_number, 'count_correct_choices':count_correct_choices}
        return render(request, 'quiz_app/questions.html', data)
    else:
        all_answers = QuizResultService(Quiz, Answers)
        result = all_answers.get_result()
        data = {'previous_number': previous_number, 'result':result}
        return render(request, 'quiz_app/result.html', data)
