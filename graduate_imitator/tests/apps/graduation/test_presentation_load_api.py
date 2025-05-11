import pytest
from rest_framework.test import APIClient
from rest_framework import status
from io import BytesIO
import os
from graduate_imitator.config.settings import BASE_DIR
from graduate_imitator.apps.graduation.domain.dto.presentation_data import PresentationData


@pytest.fixture(scope='module')
def api_client():
    return APIClient()


def test_presentation_load_api_must_return_correct_data_if_file_is_valid(api_client):
    with open(os.path.join(BASE_DIR, 'tests', 'resources', 'test_presentations', 'template.pptx'), 'rb') as file:
        file_data = BytesIO(file.read())
    response = api_client.post("/api/presentation/load", {'presentation': file_data})
    assert response.status_code == status.HTTP_200_OK
    assert PresentationData.model_validate(response.json())


def test_presentation_load_api_must_return_bad_request_error_if_file_has_invalid_type(api_client):
    with open(os.path.join(BASE_DIR, 'tests', 'resources', 'test_presentations', 'invalid_format.ppt'), 'rb') as file:
        file_data = BytesIO(file.read())
    response = api_client.post("/api/presentation/load", {'presentation': file_data})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error_msg'] == 'Bad filetype'


def test_presentation_load_api_must_return_bad_request_error_if_post_request_was_without_presentation_data(api_client):
    response = api_client.post("/api/presentation/load")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error_msg'] == 'There is no file in request'