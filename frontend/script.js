'use strict';
const API_BASE_URL = 'http://localhost:5000';
const API_CHECK_INTERVAL = 5000;
let apiCheckTimer = null;

async function checkApiStatus() {
    const statusElement = document.getElementById('api-status')
    const spinnerElement = document.getElementById('loading-spinner')
    try {
        const response = await fetch(`${API_BASE_URL}/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        if (response.ok) {
            const data = await response.json();
            statusElement.textContent = `API работает (версия ${data.version})`;
            spinnerElement.style.display = 'none';
            console.log('API сервер доступен');
        } else {
            throw new Error(`Ошибка сервера: ${response.status}`);
        }
    } catch (error) {
        if (error.message.includes('Failed to fetch')) {
            statusElement.textContent = 'API сервер недоступен'
        }
    }
}