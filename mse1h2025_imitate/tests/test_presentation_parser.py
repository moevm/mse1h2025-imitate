import os
import pytest

from parser.pptx.PresentationParser import PresentationParser
from parser.pptx.PresentationData import PresentationData
from mse1h2025_imitate.settings import BASE_DIR
from pptx.exc import PackageNotFoundError


def test_parser_must_raise_error_if_invalid_file_format():
    invalid_file_format_path = os.path.join(BASE_DIR, 'parser', 'test_presentations', 'invalid_format.ppt')
    with pytest.raises(PackageNotFoundError):
        PresentationParser.parsePPTX(invalid_file_format_path)

def test_parser_must_raise_error_if_file_does_not_exist():
    non_existing_file_path = os.path.join(BASE_DIR, 'parser', 'test_presentations', 'non_existing_file.pptx')
    with pytest.raises(PackageNotFoundError):
        PresentationParser.parsePPTX(non_existing_file_path)

def test_parser_must_return_correct_data_if_all_needed_info_exists():
    data_ = PresentationData(
        'Тема дипломной работы',
        ('Цель и задачи Актуальность: ручное распознавание  занимает '
         'слишком много времени, имеет низкую точность. Цель : автоматизировать '
         'распознавание изображений. Задачи : Задача 1 Задача 2 Задача 3 Задача 4'
        ),
        'иванов иван иванович, гр. 5381',
        ['Тема дипломной работы', 'Цель и задачи', 'Подробнее о постановке задачи', 'Задача 1',
         'Задача 2', 'Задача 3', 'Задача 4', 'Заключение', 'Апробация работы', 'Запасные слайды',
         'Практическая значимость']
    )
    parsed_data = PresentationParser.parsePPTX(os.path.join(BASE_DIR, 'parser', 'test_presentations', 'template.pptx'))
    assert data_ == parsed_data

def test_parser_must_set_topic_to_not_found_if_topic_not_found():
    presentation_data = PresentationParser.parsePPTX(os.path.join(BASE_DIR, 'parser', 'test_presentations', 'without_topic.pptx'))
    assert presentation_data.topic is not None
    assert presentation_data.topic == 'Not found'
    assert presentation_data.goalAndTasks is not None
    assert presentation_data.goalAndTasks != 'Not found'
    assert presentation_data.author is not None
    assert presentation_data.author != 'Not found'

def test_parser_must_set_author_to_not_found_if_author_not_found():
    presentation_data = PresentationParser.parsePPTX(os.path.join(BASE_DIR, 'parser', 'test_presentations', 'without_author.pptx'))
    assert presentation_data.topic is not None
    assert presentation_data.topic != 'Not found'
    assert presentation_data.goalAndTasks is not None
    assert presentation_data.goalAndTasks != 'Not found'
    assert presentation_data.author is not None
    assert presentation_data.author == 'Not found'

def test_parser_must_set_goal_and_tasks_to_not_found_if_goal_and_tasks_not_found():
    presentation_data = PresentationParser.parsePPTX(os.path.join(BASE_DIR, 'parser', 'test_presentations', 'without_goal_and_tasks.pptx'))
    assert presentation_data.topic is not None
    assert presentation_data.topic != 'Not found'
    assert presentation_data.goalAndTasks is not None
    assert presentation_data.goalAndTasks == 'Not found'
    assert presentation_data.author is not None
    assert presentation_data.author != 'Not found'

def test_parser_must_set_values_to_not_found_if_presentation_is_empty():
    presentation_data = PresentationParser.parsePPTX(os.path.join(BASE_DIR, 'parser', 'test_presentations', 'empty.pptx'))
    assert presentation_data.topic is not None
    assert presentation_data.topic == 'Not found'
    assert presentation_data.goalAndTasks is not None
    assert presentation_data.goalAndTasks == 'Not found'
    assert presentation_data.author is not None
    assert presentation_data.author == 'Not found'
    