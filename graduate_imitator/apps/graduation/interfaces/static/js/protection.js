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
            console.log('Ключевые слова:', data);
            extractedKeywords = data.keywords || [];
            window.keywords = extractedKeywords;

            if (window.keywords || window.keywords.length) {
                alert('Ключевые слова из презентации получены!');
            }

            document.getElementById('error-message').style.display = 'none';

        } else {
            showError(data.error_msg || 'Неизвестная ошибка');
        }
    } catch (error) {
        showError(error);
    }
});

function showError(error) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.style.display = 'inline-block';
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

    // Загрузка спикеров через AJAX
    fetch('/api/speaker-presets')  // Ваш endpoint для получения спикеров
        .then(response => response.json())
        .then(data => {
            const speakers = data.presets;
            const loader = document.getElementById('speakers-loader');
            const speakersList = document.getElementById('speakers-list');

            loader.style.display = 'none';
            speakersList.style.display = 'block';

            // Генерация HTML для спикеров
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

            // Обработчики событий для динамически загруженных элементов
            const speakerCards = speakersList.querySelectorAll('.speaker-card');
            const playButtons = speakersList.querySelectorAll('.play-btn');

            // Выбор спикера
            speakerCards.forEach(card => {
                card.addEventListener('click', function () {
                    speakerCards.forEach(c => c.classList.remove('selected'));
                    this.classList.add('selected');
                    document.getElementById('start-protection-btn').style.display = 'block';
                });
            });

            // Воспроизведение аудио
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

    // Выбор спикера
    speakerCards.forEach(card => {
        card.addEventListener('click', function () {
            speakerCards.forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    // Воспроизведение аудио
    playButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.stopPropagation();
            const audioFile = this.getAttribute('data-audio');
            audioPlayer.src = audioFile;
            audioPlayer.play();
        });
    });
});

document.getElementById('start-protection-btn').addEventListener('click', function () {
    const selectedSpeaker = document.querySelector('.speaker-card.selected');
    if (!selectedSpeaker) {
        alert('Пожалуйста, выберите спикера.');
        return;
    }

    if (!window.keywords || !window.keywords.length) {
        alert('Ключевые слова не найдены. Сначала обработайте презентацию.');
        return;
    }

    const keywordsStr = window.keywords.join(',');

    const speakerInfo = {
        name: selectedSpeaker.dataset.speaker,
        model_id: selectedSpeaker.dataset.model_id,
        language: selectedSpeaker.dataset.language
    };

    fetch(`/api/start-protection?keywords=${encodeURIComponent(keywordsStr)}`)
        .then(response => response.json())
        .then(data => {
            if (data.questions && Array.isArray(data.questions)) {
                sessionStorage.setItem('questions', JSON.stringify(data.questions));
                window.location.href = 'api/answer';
            } else {
                alert('Не удалось получить вопросы.');
            }
        })
});