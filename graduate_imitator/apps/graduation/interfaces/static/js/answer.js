document.addEventListener("DOMContentLoaded", function () {
    const dataElement = document.getElementById('answer-data');

    const container = document.querySelector('.questions-block');
    const template = document.getElementById('question-template');

    if (!questions.length) {
        document.getElementById('error-message').style.display = 'block';
        document.querySelector('#error-message p').textContent = 'Вопросы не найдены. Попробуйте начать защиту заново.';
        return;
    }

    questions.forEach(question => {
        const clone = template.content.cloneNode(true);
        const questionEl = clone.querySelector('.generated-question');
        const toggle = questionEl.querySelector('.question-toggle');
        const text = questionEl.querySelector('.question-text');

        toggle.addEventListener('click', () => {
            text.classList.toggle('hidden');
            toggle.innerText = text.classList.contains('hidden')
                ? '🔽 Посмотреть текст вопроса'
                : '🔼 Скрыть текст вопроса';
        });

        questionEl.querySelector('.question-text').textContent = question.question_text;

        const startBtn = clone.querySelector('.start-record-btn');
        const stopBtn = clone.querySelector('.stop-record-btn');
        const indicator = clone.querySelector('.recording-indicator');

        startBtn.addEventListener('click', () => {
            stopBtn.style.display = 'inline-block';
            indicator.style.display = 'block';
        });

        stopBtn.addEventListener('click', () => {
            stopBtn.style.display = 'none';
            indicator.style.display = 'none';
            startBtn.style.display = 'inline-block';
        });

        container.appendChild(clone);
    });
})

document.addEventListener('DOMContentLoaded', function () {
    const playBtn = document.querySelector('.play-audio-btn');
    const questionText = document.querySelector('.question-text').innerText;
    const audioPlayer = document.getElementById('speaker-audio-player');

    playBtn.addEventListener('click', async function () {
        if (playBtn.dataset.audioLoaded === 'true') {
            audioPlayer.play();
            return;
        }

        try {
            playBtn.disabled = true;
            playBtn.textContent = '⏳ Готовим...';

            const response = await fetch('/api/text-to-speech/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    text: questionText,
                    speaker: speakerInfo.name,
                    model_id: speakerInfo.model_id,
                    language: speakerInfo.language
                })
            });

            if (!response.ok) {
                throw new Error('Ошибка запроса к TTS API');
            }

            const data = await response.json();
            const audioSrc = data.question_tts.audio_sample;

            audioPlayer.src = audioSrc;
            playBtn.dataset.audioLoaded = 'true';
            audioPlayer.play();

        } catch (error) {
            console.error('Ошибка при воспроизведении:', error);
            alert("Ошибка при генерации речи. Попробуй позже.");
        } finally {
            // Верни кнопку
            playBtn.disabled = false;
            playBtn.textContent = '🔊 Слушать';
        }
    });
});

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