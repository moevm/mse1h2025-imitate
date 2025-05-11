async function loadResults() {
    try {
        const response = await fetch('/api/get-results', { credentials: 'include' });
        if (!response.ok) {
            throw new Error('Ошибка при получении результатов');
        }
        const data = await response.json();
        const resultsBody = document.getElementById('results-body');
        resultsBody.innerHTML = '';

        if (data.results && data.results.length > 0) {
            data.results.forEach(item => {
                const row = document.createElement('tr');
                const dateCell = document.createElement('td');
                const scoreCell = document.createElement('td');

                dateCell.textContent = item.date;
                scoreCell.textContent = item.score;

                row.appendChild(dateCell);
                row.appendChild(scoreCell);
                resultsBody.appendChild(row);
            });
        } else {
            resultsBody.innerHTML = '<tr><td colspan="2">Нет данных</td></tr>';
        }
    } catch (error) {
        console.error('Ошибка загрузки результатов:', error);
    }
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

window.addEventListener('DOMContentLoaded', loadResults);


document.addEventListener('DOMContentLoaded', function() {
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
                card.addEventListener('click', function() {
                    speakerCards.forEach(c => c.classList.remove('selected'));
                    this.classList.add('selected');
                });
            });
            
            // Воспроизведение аудио
            playButtons.forEach(button => {
                button.addEventListener('click', function(e) {
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


document.addEventListener('DOMContentLoaded', function() {
    const speakerCards = document.querySelectorAll('.speaker-card');
    const audioPlayer = document.getElementById('speaker-audio-player');
    const playButtons = document.querySelectorAll('.play-btn');
    
    // Выбор спикера
    speakerCards.forEach(card => {
        card.addEventListener('click', function() {
            speakerCards.forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
        });
    });
    
    // Воспроизведение аудио
    playButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const audioFile = this.getAttribute('data-audio');
            audioPlayer.src = audioFile;
            audioPlayer.play();
        });
    });
});