import pytest
from rest_framework.test import APIClient


@pytest.fixture(scope='module')
def api_client():
    return APIClient()


def test_speaker_presets_api_must_return_array_with_demo(api_client):
    response = api_client.get("/api/speaker-presets").json()
    assert 'presets' in response
    assert isinstance(response['presets'], list)
    assert len(response['presets']) > 0
    for preset in response['presets']:
        assert 'name' in preset
        assert 'model_id' in preset
        assert 'language' in preset
        assert 'audio_sample' in preset