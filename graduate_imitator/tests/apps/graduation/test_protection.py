import pytest
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.permissions import AllowAny
from graduate_imitator.apps.graduation.domain.repositories.question_repository import QuestionRepository
from graduate_imitator.apps.graduation.api.views.protection_api import StartProtectionAPIView

@pytest.fixture(autouse=True)
def allow_any(monkeypatch):
    monkeypatch.setattr(
        StartProtectionAPIView,
        "permission_classes",
        [AllowAny]
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def url():
    return "/api/start-protection"

def make_question(id_, text):
    return {"id": id_, "text": text}

def test_start_protection_success(api_client, url, monkeypatch):
    sample_questions = [make_question(1, "Вопрос 1"), make_question(2, "Вопрос 2")]
    monkeypatch.setattr(
        QuestionRepository,
        "get_questions_by_keywords_any",
        classmethod(lambda cls, kws: sample_questions)
    )

    response = api_client.get(url, {"keywords": "math,physics"})
    assert response.status_code == status.HTTP_200_OK, response.content
    data = response.json()
    assert "message" in data and data["message"] == "Защита началась"
    assert "questions" in data
    assert isinstance(data["questions"], list)
    assert data["questions"] == sample_questions

def test_start_protection_no_keywords_returns_empty_list(api_client, url, monkeypatch):
    monkeypatch.setattr(
        QuestionRepository,
        "get_questions_by_keywords_any",
        classmethod(lambda cls, kws: [])
    )

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["questions"] == []
    assert data["message"] == "Защита началась"

def test_start_protection_internal_error(api_client, url, monkeypatch):
    def raise_exc(cls, kws):
        raise RuntimeError("БД недоступна")
    monkeypatch.setattr(
        QuestionRepository,
        "get_questions_by_keywords_any",
        classmethod(raise_exc)
    )

    response = api_client.get(url, {"keywords": "any"})
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert "error" in data
    assert "БД недоступна" in data["error"]

@pytest.mark.parametrize("raw_kw,expected", [
    ("one", ["one"]),
    ("one,two,  three ", ["one", "two", "three"]),
    ("", []),
])
def test_keyword_parsing(monkeypatch, raw_kw, expected):
    request = type("Req", (), {})()
    request.query_params = {"keywords": raw_kw}
    captured = []
    monkeypatch.setattr(
        QuestionRepository,
        "get_questions_by_keywords_any",
        classmethod(lambda cls, kws: captured.extend(kws) or [])
    )
    view = StartProtectionAPIView()
    response = view.get(request)
    assert captured == expected
    assert response.status_code == status.HTTP_200_OK
