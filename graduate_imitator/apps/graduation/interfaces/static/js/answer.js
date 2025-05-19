document.addEventListener("DOMContentLoaded", function () {
    const questions = JSON.parse(sessionStorage.getItem('questions') || '[]');
    const container = document.querySelector('.questions-block');
    const template = document.getElementById('question-template');

    if (!questions.length) {
        document.getElementById('error-message').style.display = 'block';
        document.querySelector('#error-message p').textContent = 'Вопросы не найдены. Попробуйте начать защиту заново.';
        return;
    }

    questions.forEach(question => {
        const clone = template.content.cloneNode(true);
        clone.querySelector('.question-text').textContent = question.question_text;

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
});