from django.core.cache import cache
from .models import Topic, Question, Answer
import json
import logging
from random import sample


def put_correct_answer_ids_to_cache(topic_id):
    """
    Зберігає ID правильних відповідей у кеш для заданої теми.
    """
    # Отримуємо ID правильних відповідей для питань цієї теми
    correct_answers_id = list(
        Answer.objects.filter(
            question_id__topic_id=topic_id,
            is_correct=True
        ).values_list('id', flat=True)
    )

    # Зберігаємо список у кеш з ключем, специфічним для теми
    data_to_json = json.dumps(correct_answers_id)
    cache.set(f'correct_answer_{topic_id}', data_to_json, timeout=1800)

    return correct_answers_id


def put_topic_questions_and_answers_to_cache(topic_id):
    """Беремо всі запитання і відповіді відповідної теми та кладемо в кеш"""
    try:
        # Отримати питання, пов'язані з темою
        questions = Question.objects.filter(topic_id=topic_id)

        # Отримати всі відповіді, пов'язані з питаннями цієї теми
        answers = Answer.objects.filter(question_id__in=[question.id for question in questions])

        # Створити словник для питань та відповідей
        data = []

        # Створити словник з відповідями для кожного питання
        answers_dict = {}
        for answer in answers:
            if answer.question_id.id not in answers_dict:
                answers_dict[answer.question_id.id] = []
            answers_dict[answer.question_id.id].append({
                'ans_id': answer.id,
                'ans_text': answer.answer_text,
                'is_correct': answer.is_correct,
                'img_ref': answer.img_ref.name if answer.img_ref.name != 'NULL' else None
            })

        for question in questions:
            data.append({
                'question_id': question.id,
                'question_text': question.question_text,
                'img_ref': question.img_ref.name if question.img_ref.name != 'NULL' else None,
                'answers': answers_dict.get(question.id, [])
            })

        data_to_json = json.dumps(data)
        cache.set(f'data_topic_{topic_id}', data_to_json, timeout=1800)

        return data

    except Exception as e:
        logging.error(f"Error fetching content: {e}")
        return []


def get_content_from_cache(content_type):
    """Перевіряємо чи є необхідні дані в кеші"""
    try:
        content_in_json_cache = cache.get(content_type)

        if content_in_json_cache:
            return json.loads(content_in_json_cache)

        else:
            return None

    except Exception as e:
        logging.error(f"Error fetching content: {e}")
        return []


def put_topic_data_to_cache():
    """Кладемо всю інформацію по темах в кеш"""
    try:
        topics_form_db = Topic.objects.values_list('title', 'time_to_pass', 'is_open', 'question_in_test',
                                                   'id')
        topics = []

        for title, time_to_pass, is_open, question_in_test, topic_id in topics_form_db:
            time_in_minutes = time_to_pass.seconds // 60
            words = title.split('_')
            converted_title = ' '.join(word.capitalize() for word in words)

            topics.append({'title': converted_title, 'time_to_pass': time_in_minutes, 'is_open': is_open,
                           'question_in_test': question_in_test, 'topic_id': topic_id})

        # Перетворимо дані в JSON та збережемо їх в кеш з часом життя 300 секунд
        topics_to_json = json.dumps(topics)
        cache.set('topics', topics_to_json, timeout=300)

        return topics

    except Exception as e:
        logging.error(f"Error entering topic data: {e}")
        return []


def get_random_questions(topic_id, need_questions):
    """
    Випадково обирає задану кількість питань для відповідної теми з кешу.
    Також перемішує відповіді в кожному питанні.
    """
    # Отримуємо дані з кешу або завантажуємо їх
    data = get_content_from_cache(f'data_topic_{topic_id}')
    if data is None:
        data = put_topic_questions_and_answers_to_cache(topic_id)

    # Перевіряємо, чи достатньо питань для вибірки
    num_of_questions = len(data)
    if need_questions > num_of_questions:
        raise ValueError(f"Requested {need_questions} questions, but only {num_of_questions} are available.")

    # Обираємо випадкові питання та перемішуємо відповіді
    selected_questions = sample(data, need_questions)
    for question in selected_questions:
        question['answers'] = sample(question['answers'], len(question['answers']))

    return selected_questions
