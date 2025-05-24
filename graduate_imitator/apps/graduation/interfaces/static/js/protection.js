document.getElementById('process-btn').addEventListener('click', async () => {
    const fileInput = document.getElementById('presentation-upload');
    const file = fileInput.files[0];

    if (!file) {
        alert('Пожалуйста, выберите файл презентации.');
        return;
    }

    const formData = new FormData();
    formData.append('presentation', file);

    try {
        const csrfToken = getCookie('csrftoken');
        const response = await fetch('/api/presentation/extract_keywords', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        });

        const data = await response.json();

        if (response.ok) {
            console.log('API Response from extract_keywords:', data);

            extractedKeywords = data.keywords || [];
            window.keywords = extractedKeywords;
            if (typeof data.presentation_id !== 'undefined' && data.presentation_id !== null && data.presentation_id !== '') {
                window.presentationId = data.presentation_id;
            } else {
                window.presentationId = null;
                console.error('Presentation ID not received from API or is empty/invalid.', data.presentation_id);
                showError('ID презентации не был получен от сервера или имеет неверный формат. Попробуйте еще раз.');
                return;
            }

            if (window.keywords && window.keywords.length) {
                alert('Презентация успешно обработана!');
            } else {
                alert('Презентация обработана. Ключевые слова извлечь не удалось.');
            }

            document.getElementById('process-btn').disabled = true;

        } else {
            showError(data.error_msg || 'Неизвестная ошибка при обработке презентации.');
        }
    } catch (error) {
        console.error('Error processing presentation:', error);
        showError('Ошибка сети или внутренняя ошибка сервера при обработке презентации.');
    }
});

function showError(error) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.style.display = 'block';
    errorDiv.querySelector('p').textContent = 'Ошибка: ' + error;

    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    const audioPlayer = document.getElementById('speaker-audio-player');

    fetch('/api/speaker-presets') 
        .then(response => response.json())
        .then(data => {
            const speakers = data.presets;
            const loader = document.getElementById('speakers-loader');
            const speakersList = document.getElementById('speakers-list');

            loader.style.display = 'none';
            speakersList.style.display = 'block';

            speakersList.innerHTML = speakers.map(speaker => `
                <div class="speaker-card" data-speaker="${speaker.name}" data-model_id="${speaker.model_id}" data-language="${speaker.language}">
                    <div class="speaker-info">
                        <h4>${speaker.name}</h4>
                    </div>
                    <button class="play-btn" data-audio="${speaker.audio_sample}">
                        <i class="fas fa-play"></i>
                    </button>
                </div>
            `).join('');

            const speakerCards = speakersList.querySelectorAll('.speaker-card');
            const playButtons = speakersList.querySelectorAll('.play-btn');

            speakerCards.forEach(card => {
                card.addEventListener('click', function () {
                    speakerCards.forEach(c => c.classList.remove('selected'));
                    this.classList.add('selected');
                    document.getElementById('start-protection-btn').style.display = 'block';
                });
            });

            playButtons.forEach(button => {
                button.addEventListener('click', function (e) {
                    e.stopPropagation();
                    const audioFile = this.getAttribute('data-audio');
                    audioPlayer.src = audioFile;
                    audioPlayer.play();
                });
            });
        })
        .catch(error => {
            console.error('Ошибка загрузки спикеров:', error);
            document.getElementById('speakers-loader').innerHTML =
                '<p class="error-text">Не удалось загрузить спикеров</p>';
        });
});

document.addEventListener('DOMContentLoaded', function () {
    const speakerCards = document.querySelectorAll('.speaker-card');
    const audioPlayer = document.getElementById('speaker-audio-player');
    const playButtons = document.querySelectorAll('.play-btn');

    speakerCards.forEach(card => {
        card.addEventListener('click', function () {
            speakerCards.forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    playButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.stopPropagation();
            const audioFile = this.getAttribute('data-audio');
            audioPlayer.src = audioFile;
            audioPlayer.play();
        });
    });
});

document.getElementById('start-protection-btn').addEventListener('click', async function (event) {
    event.preventDefault();
    const selectedSpeaker = document.querySelector('.speaker-card.selected');
    
    if (!selectedSpeaker) {
        alert('Пожалуйста, выберите спикера.');
        return;
    }

    if (!Array.isArray(window.keywords) || window.keywords.length === 0) {
        alert('Ключевые слова не найдены. Сначала обработайте презентацию.');
        return;
    }

    if (typeof window.presentationId === 'undefined' || window.presentationId === null || window.presentationId === '' || isNaN(parseInt(window.presentationId))) {
        alert('ID презентации не найден, пуст или некорректен. Пожалуйста, сначала успешно обработайте презентацию.');
        console.error('window.presentationId is missing, empty, or not a number before submitting to AnswerWebView. Value:', window.presentationId);
        return;
    }

    const keywordsStr = window.keywords.join(',');

    const speakerInfo = {
        name: selectedSpeaker.dataset.speaker,
        model_id: selectedSpeaker.dataset.model_id,
        language: selectedSpeaker.dataset.language
    };

    try {
        const response = await fetch(`/api/start-protection?keywords=${encodeURIComponent(keywordsStr)}`);
        const data = await response.json();

        if (response.ok && data.questions && Array.isArray(data.questions)) {
            document.getElementById('questions-input').value = JSON.stringify(data.questions);
            document.getElementById('speaker-input').value = JSON.stringify(speakerInfo);
            document.getElementById('presentation-id-input').value = window.presentationId;
            
            document.getElementById('to-answer-form').submit();
        } else {
            alert('Не удалось получить вопросы от /api/start-protection. ' + (data.error || ''));
            console.error('Error fetching questions:', data);
        }
    } catch (error) {
        alert('Ошибка при получении вопросов для начала защиты.');
        console.error('Network or other error in start-protection fetch:', error);
    }
});