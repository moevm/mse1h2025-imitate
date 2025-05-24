document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector('.questions-block');
    const template = document.getElementById('question-template');
    const answersData = []; // для хранения всех ответов

    // Предполагается, что currentPresentationId будет доступен глобально,
    // установлен Django темплейтом, как questions и speakerInfo
    let attemptStartTime = null; // Будет установлено при показе первого вопроса

    console.log('questions=', questions);
    console.log('speakerInfo=', speakerInfo);

    if (!questions.length) {
        document.getElementById('error-message').style.display = 'inline-block';
        document.querySelector('#error-message p').textContent = 'Вопросы не найдены. Попробуйте начать защиту заново.';
        return;
    }

    let currentQuestionIndex = 0;

    function showNextQuestion() {
        if (currentQuestionIndex === 0) {
            attemptStartTime = new Date().toISOString(); // Фиксируем время начала первой попытки вопроса
        }

        const question = questions[currentQuestionIndex];
        const clone = template.content.cloneNode(true);
        const questionEl = clone.querySelector('.question-container');
        const effectsContainer = clone.querySelector('.effects-container');

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

        let mediaRecorder;
        let audioChunks = [];

        // Фиксирование времени ответа
        let questionPlayTime = null;  // когда воспроизводили вопрос
        let recordStartTime = null;  // когда начали запись
        let recordStopTime = null;  // когда остановили запись

        // Кнопка слушать
        const playBtn = clone.querySelector('.play-audio-btn');
        const answerIsGiven = clone.querySelector('.answer-is-given');
        const questionText = clone.querySelector('.question-text').innerText;
        const audioPlayer = clone.getElementById('speaker-audio-player');
        playBtn.addEventListener('click', async function () {
            if (playBtn.dataset.audioLoaded === 'true') {
                audioPlayer.play();
                return;
            }

            try {

                var effects = effectsContainer.querySelectorAll('.effect-card input');
                var effects_values = [];
                effects.forEach(effect => {
                    if(effect.getAttribute('type') == 'range'){
                        effects_values.push(parseFloat(effect.value));
                    } else{
                        effects_values.push(effect.checked);
                    }
                    
                });
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
                        language: speakerInfo.language,
                        effects: effects_values
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
                alert("Ошибка при генерации речи.");
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

                    currentQuestionIndex += 1;

                    if (currentQuestionIndex < questions.length) {
                        showNextQuestion();
                    } else {
                        // Все вопросы пройдены — показываем кнопку и аудиоплеер
                        setupAudioReview();
                    }
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
            startBtn.style.display = "none";
            answerIsGiven.style.display = "block";
            stopBtn.style.display = 'none';
            indicator.style.display = 'none';
        });

        container.appendChild(clone);
    }

    function setupAudioReview() {
        const reviewBlock = document.querySelector('.audio-review-block');
        const finishBtn = document.querySelector('.finish-protection-btn');
        const endProtectionBlock = document.querySelector('.end-protection-block');

        endProtectionBlock.style.display = "inline-block";

        reviewBlock.innerHTML = '';

        answersData.forEach((answer, index) => {
            const wrapper = document.createElement('div');
            wrapper.classList.add('audio-answer-wrapper');
            wrapper.style.marginBottom = '1em';

            const label = document.createElement('p');
            label.textContent = `Запись ответа на вопрос №${index + 1}`;
            label.style.fontWeight = 'bold';

            const audio = document.createElement('audio');
            audio.controls = true;
            audio.src = URL.createObjectURL(answer.audioBlob);

            wrapper.appendChild(label);
            wrapper.appendChild(audio);
            reviewBlock.appendChild(wrapper);
        });

        reviewBlock.style.display = 'block';
        finishBtn.style.display = 'block';

        finishBtn.onclick = () => {
            const formData = new FormData();

            if (typeof currentPresentationId === 'undefined' || currentPresentationId === null) {
                alert("Ошибка: ID презентации не найден. Невозможно сохранить попытку.");
                console.error("presentation_id is missing, cannot save attempt.");
                return; // Прерываем отправку
            }
            if (!attemptStartTime) {
                alert("Ошибка: Время начала попытки не найдено. Невозможно сохранить попытку.");
                console.error("start_time is missing, cannot save attempt.");
                return; // Прерываем отправку
            }

            answersData.forEach((answer, index) => {
                formData.append(`answers[${index}][question_id]`, answer.question_id);
                formData.append(`answers[${index}][responseDelay]`, answer.responseDelay);
                formData.append(`answers[${index}][responseDuration]`, answer.responseDuration);
                formData.append(`answers[${index}][audioBlob]`, answer.audioBlob);
            });

            formData.append(`length`, answersData.length);
            formData.append('presentation_id', currentPresentationId);
            formData.append('start_time', attemptStartTime);

            const csrfToken = getCookie('csrftoken');

            fetch('api/analyze_answers', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(response => {
                window.location.href = response.url;
            })
            .then(data => {
                if (data?.error) {
                    alert("Ошибка анализа: " + data.error);
                }
            })
            .catch(error => {
                console.error('Ошибка при отправке данных:', error);
            });
        };
    }

    showNextQuestion();
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