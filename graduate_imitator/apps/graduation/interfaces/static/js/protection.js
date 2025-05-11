let extractedKeywords = [];

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
        const response = await fetch('/api/presentation/load', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        });

        const data = await response.json();

        if (response.ok) {
            console.log('Ключевые слова:', data);
            extractedKeywords = data.topic || [];
            document.getElementById('error-message').style.display = 'none';
            document.getElementById('start-protection-btn').style.display = 'inline-block';

        } else {
            showError(data.error_msg || 'Неизвестная ошибка');
        }
    } catch (error) {
        showError(error);
    }
});

document.getElementById('start-protection-btn').addEventListener('click', async () => {
    if (!extractedKeywords.length) {
        alert('Нет ключевых слов для отправки.');
        return;
    }

    try {
        const csrfToken = getCookie('csrftoken');
        const response = await fetch('/api/start-protection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                keywords: extractedKeywords,
                language: 'ru',
                model_id: 'default',
                speaker: 'default'
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert('Защита началась! Получено вопросов: ' + data.questions.length);
        } else {
            showError(data.error || 'Ошибка запуска защиты');
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