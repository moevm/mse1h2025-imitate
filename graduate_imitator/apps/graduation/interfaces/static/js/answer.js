document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector('.questions-block');
    const template = document.getElementById('question-template');
    const answersData = []; // для хранения всех ответов

    if (!questions.length) {
        document.getElementById('error-message').style.display = 'block';
        document.querySelector('#error-message p').textContent = 'Вопросы не найдены. Попробуйте начать защиту заново.';
        return;
    }

    questions.forEach(question => {
        const clone = template.content.cloneNode(true);
        const questionEl = clone.querySelector('.generated-question');

        // номер вопроса
        const questionNumberHeader = document.createElement('h3');
        questionNumberHeader.textContent = `Вопрос №${questions.indexOf(question) + 1}`;
        questionNumberHeader.classList.add('centered-content');
        questionEl.prepend(questionNumberHeader);

        // выпадашка с текстом вопроса
        const toggle = questionEl.querySelector('.question-toggle');
        const text = questionEl.querySelector('.question-text');
        toggle.addEventListener('click', () => {
            text.classList.toggle('hidden');
            toggle.innerText = text.classList.contains('hidden')
                ? '🔽 Посмотреть текст вопроса'
                : '🔼 Скрыть текст вопроса';
        });
        text.textContent = question.question_text;

        const startBtn = clone.querySelector('.start-record-btn');
        const stopBtn = clone.querySelector('.stop-record-btn');
        const indicator = clone.querySelector('.recording-indicator');
        const reviewBlock = document.querySelector('.audio-review-block');
        const player = document.querySelector('.recorded-answer-player');
        const finishBtn = document.querySelector('.finish-protection-btn');

        let mediaRecorder;
        let audioChunks = [];

        // Фиксирование времени ответа
        let questionPlayTime = null;  // когда воспроизводили вопрос
        let recordStartTime = null;  // когда начали запись
        let recordStopTime = null;  // когда остановили запись

        // Кнопка слушать
        const playBtn = clone.querySelector('.play-audio-btn');
        const questionText = clone.querySelector('.question-text').innerText;
        const audioPlayer = clone.getElementById('speaker-audio-player');
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
                questionPlayTime = new Date();  // фиксируем воспроизведение вопроса

            } catch (error) {
                console.error('Ошибка при воспроизведении:', error);
                alert("Ошибка при генерации речи. Попробуй позже.");
            } finally {
                playBtn.disabled = false;
                playBtn.textContent = '🔊 Слушать';
            }
        });

        // Кнопка начать запись
        startBtn.addEventListener('click', async () => {
            recordStartTime = new Date();  // фиксируем старт записи
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = e => {
                    if (e.data.size > 0) {
                        audioChunks.push(e.data);
                    }
                };

                mediaRecorder.onstop = () => {
                    recordStopTime = new Date();  // фиксируем остановку

                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    player.src = audioUrl;
                    reviewBlock.style.display = 'block';

                    // Метрики
                    const responseDelay = questionPlayTime
                        ? ((recordStartTime - questionPlayTime) / 1000).toFixed(2)
                        : null;
                    const responseDuration = ((recordStopTime - recordStartTime) / 1000).toFixed(2);

                    answersData.push({
                        question_id: question.id,
                        audioBlob: audioBlob,
                        responseDelay: responseDelay,
                        responseDuration: responseDuration
                    });


                    // пока просто логируем для отправки в будущем
                    finishBtn.onclick = () => {
                        console.log('Все собранные ответы:');
                        answersData.forEach((answer, idx) => {
                            console.log('question_id:', answer.question_id);
                            console.log('audioBlob:', answer.audioBlob);
                            console.log('responseDelay (сек):', answer.responseDelay);
                            console.log('responseDuration (сек):', answer.responseDuration);
                            console.log('-----------------------------');
                        });
                    };
                };

                mediaRecorder.start();
                stopBtn.style.display = 'inline-block';
                indicator.style.display = 'block';
            } catch (error) {
                console.error('Ошибка доступа к микрофону:', error);
                alert('Не удалось получить доступ к микрофону.');
            }
        });

        stopBtn.addEventListener('click', () => {
            mediaRecorder?.stop();
            stopBtn.style.display = 'none';
            indicator.style.display = 'none';
        });

        container.appendChild(clone);
    });
})

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