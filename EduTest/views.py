from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
import logging
from .models import UserProfile, Result
from .services import put_topic_data_to_cache, get_content_from_cache, get_random_questions, put_correct_answer_ids_to_cache


def index(request):
    topics = get_content_from_cache('topics')

    if topics is None:
        topics = put_topic_data_to_cache()

    return render(request, 'EduTest/index.html', {'topics': topics})


def one_time_registration(request):
    if request.method == 'POST':
        topic_id = int(request.POST.get('topic_id'))
        title = request.POST.get('title')

        if topic_id:
            topics_data = get_content_from_cache('topics')

            if topics_data is None:
                topics_data = put_topic_data_to_cache()

            for data in topics_data:
                if topic_id == data['topic_id']:
                    if data['is_open'] is True:
                        return render(request, 'EduTest/one_time_registration.html',
                                      {'title': title, 'topic_id': topic_id})
                    else:
                        logging.info("Зараз тема закрита для проходження")
                        return redirect('/')
            logging.info("Немає такого topic_id якій надійшов від форми в кешованому списку")
            return redirect('/')
        else:
            logging.info("У формі немає поля input з topic_id")
            return redirect('/')

    else:
        logging.info("Відсутній POST метод при запиті")
        return redirect('/')


def testing(request):
    if request.method == 'POST':
        topic_id = int(request.POST.get('topic_id'))
        title = request.POST.get('title')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        group = request.POST.get('group')

        if topic_id and title:
            topics_data = get_content_from_cache('topics')

            if topics_data is None:
                topics_data = put_topic_data_to_cache()

            for topic in topics_data:
                if topic['topic_id'] == topic_id:
                    if topic['is_open'] is True:
                        question_need = topic['question_in_test']

                        data = get_random_questions(topic_id, question_need)

                        return render(request, 'EduTest/testing.html',
                                      {'data': data, 'topic_id': topic_id, 'name': name, 'surname': surname, 'group': group})

                    else:
                        logging.info("Зараз тема закрита для проходження")
                        return redirect('/')

            logging.info("Немає такого topic_id якій надійшов від форми в кешованому списку")
            return redirect('/')

        else:
            logging.info("Відсутній id теми або назва")
            return redirect('/')

    else:
        logging.info("Відсутній POST метод при запиті")
        return redirect('/')


def calculate_result(request):
    if request.method == 'POST':
        user_answers = request.POST
        topic_id = int(user_answers.get('topic_id'))
        first_name = user_answers.get('name')
        last_name = user_answers.get('surname')
        group_name = user_answers.get('group')

        # Перевіряємо чи існує користувач
        user_profile, created = UserProfile.objects.get_or_create(
            first_name=first_name,
            last_name=last_name,
            group_name=group_name
        )

        user_answers_id = [
            int(value) for key, value in user_answers.items() if key.startswith('question_')
        ]

        correct_answers_id = get_content_from_cache(f'correct_answer_{topic_id}') or put_correct_answer_ids_to_cache(topic_id)

        # Підраховуємо кількість правильних відповідей
        user_correct_count = sum(1 for answer in user_answers_id if answer in correct_answers_id)

        # Отримуємо кількість питань у тесті
        topics = get_content_from_cache('topics') or put_topic_data_to_cache()
        questions_count = next((topic['question_in_test'] for topic in topics if topic['topic_id'] == topic_id), 0)

        test_result_percentage = (user_correct_count * 100) // questions_count if questions_count > 0 else 0

        # Зберігаємо результат тестування у таблицю Result
        Result.objects.create(
            user_id=user_profile,
            topic_id_id=topic_id,
            score=test_result_percentage
        )

    return redirect('/')


def select_table_score(request):
    topics = get_content_from_cache('topics')

    if topics is None:
        topics = put_topic_data_to_cache()
    return render(request, 'EduTest/select_table_score.html', {'topics': topics})


def table_score(request):
    if request.method == 'POST':
        selected_topic_id = request.POST.get('topics')

        results = Result.objects.filter(topic_id=selected_topic_id).select_related('user_id')

        students = [
            {
                'name': f"{result.user_id.first_name} {result.user_id.last_name}",
                'group': result.user_id.group_name,
                'score': result.score,
                'time': result.passed_at.strftime("%Y-%m-%d %H:%M")
            } for result in results
        ]

        return render(request, 'EduTest/table_score.html', {'students': students})

    else:
        return redirect('/')


def page_not_found(request, exception):
    return HttpResponseNotFound('Сторінка відсутня')