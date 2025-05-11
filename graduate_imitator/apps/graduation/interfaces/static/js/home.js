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
