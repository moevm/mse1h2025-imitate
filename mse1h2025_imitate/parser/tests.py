from django.test import TestCase
from .pptx.PresentationParser import PresentationParser
from .pptx.PresentationData import PresentationData
from mse1h2025_imitate.settings import BASE_DIR
import os

from pptx.exc import PackageNotFoundError


class PresentationParserTestCase(TestCase):

    def testInvalidFileFormat(self):
        invalidFileFormatPath = os.path.join(BASE_DIR, 'parser', 'test_presentations', 'invalid_format.ppt')
        self.assertRaises(PackageNotFoundError, PresentationParser.parsePPTX, invalidFileFormatPath)

    def testFileDoesNotExists(self):
        nonExistingFilePath = os.path.join(BASE_DIR, 'parser', 'test_presentations', 'non_existing_file.pptx')
        self.assertRaises(PackageNotFoundError, PresentationParser.parsePPTX, nonExistingFilePath)

    def testAllNeededInfoInPresentationExists(self):
        data_ = PresentationData(
            'Тема дипломной работы',
            ('Цель и задачи Актуальность: ручное распознавание  занимает '
             'слишком много времени, имеет низкую точность. Цель : автоматизировать '
             'распознавание изображений. Задачи : Задача 1 Задача 2 Задача 3 Задача 4'
            ),
            'иванов иван иванович, гр. 5381'
        )
        self.assertEqual(
            data_,
            PresentationParser.parsePPTX(os.path.join(BASE_DIR, 'parser', 'test_presentations', 'template.pptx'))
        )

    def testPresentationWithoutTopic(self):
        presentationData =  PresentationParser.parsePPTX(os.path.join(BASE_DIR, 'parser', 'test_presentations', 'without_topic.pptx'))
        self.assertIsNotNone(presentationData.topic)
        self.assertEqual('Not found', presentationData.topic)
        self.assertIsNotNone(presentationData.goalAndTasks)
        self.assertNotEqual('Not found', presentationData.goalAndTasks)
        self.assertIsNotNone(presentationData.author)
        self.assertNotEqual('Not found', presentationData.author)

    def testPresentationWithoutAuthor(self):
        presentationData =  PresentationParser.parsePPTX(os.path.join(BASE_DIR, 'parser', 'test_presentations', 'without_author.pptx'))
        self.assertIsNotNone(presentationData.topic)
        self.assertNotEqual('Not found', presentationData.topic)
        self.assertIsNotNone(presentationData.goalAndTasks)
        self.assertNotEqual('Not found', presentationData.goalAndTasks)
        self.assertIsNotNone(presentationData.author)
        self.assertEqual('Not found', presentationData.author)

    def testPresentationWithoutGoalAndTasks(self):
        presentationData =  PresentationParser.parsePPTX(os.path.join(BASE_DIR, 'parser', 'test_presentations', 'without_goal_and_tasks.pptx'))
        self.assertIsNotNone(presentationData.topic)
        self.assertNotEqual('Not found', presentationData.topic)
        self.assertIsNotNone(presentationData.goalAndTasks)
        self.assertEqual('Not found', presentationData.goalAndTasks)
        self.assertIsNotNone(presentationData.author)
        self.assertNotEqual('Not found', presentationData.author)

    def testEmptyPresentation(self):
        presentationData =  PresentationParser.parsePPTX(os.path.join(BASE_DIR, 'parser', 'test_presentations', 'empty.pptx'))
        self.assertIsNotNone(presentationData.topic)
        self.assertEqual('Not found', presentationData.topic)
        self.assertIsNotNone(presentationData.goalAndTasks)
        self.assertEqual('Not found', presentationData.goalAndTasks)
        self.assertIsNotNone(presentationData.author)
        self.assertEqual('Not found', presentationData.author)