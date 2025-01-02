from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
import logging
from .services import put_topic_data_to_cache, get_content_from_cache, put_topic_questions_and_answers_to_cache


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
                if topic_id in data:
                    if data[2] is True:
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

        if topic_id and title:
            data = get_content_from_cache(f'data_topic_{topic_id}')

            if data is None:
                data = put_topic_questions_and_answers_to_cache(topic_id)

            return render(request, 'EduTest/testing.html',
                          {'data': data})

        else:
            logging.info("Відсутній id теми або назва")
            return redirect('/')

    else:
        logging.info("Відсутній POST метод при запиті")
        return redirect('/')


def select_table_score(request):
    return render(request, 'EduTest/select_table_score.html')


def table_score(request):
    return render(request, 'EduTest/table_score.html')


def page_not_found(request, exception):
    return HttpResponseNotFound('Сторінка відсутня')
