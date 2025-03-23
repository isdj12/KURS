document.addEventListener('DOMContentLoaded', function() {
    // Получить модальное окно
    var modal = document.getElementById("soo");

    // Получить кнопку, которая открывает модальное окно
    var btn = document.getElementById("openModalBtn");

    var span = document.getElementsByClassName("close")[0];

    if (btn) {
        btn.onclick = function() {
            modal.style.display = "block";
        }
    }

    if (span) {
        span.onclick = function() {
            modal.style.display = "none";
        }
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Проверка доступности логина и email
    const loginInput = document.getElementById('login');
    const emailInput = document.getElementById('pochta');
    const loginFeedback = document.createElement('div');
    const emailFeedback = document.createElement('div');
    
    // Добавляем элементы обратной связи после полей ввода
    if (loginInput) {
        loginInput.insertAdjacentElement('afterend', loginFeedback);
        loginInput.addEventListener('blur', function() {
            checkAvailability('login', loginInput.value, loginFeedback);
        });
    }
    
    if (emailInput) {
        emailInput.insertAdjacentElement('afterend', emailFeedback);
        emailInput.addEventListener('blur', function() {
            checkAvailability('email', emailInput.value, emailFeedback);
        });
    }
    
    function checkAvailability(type, value, feedbackElement) {
        if (!value) {
            feedbackElement.textContent = '';
            return;
        }
        
        // Проверяем корректность email
        if (type === 'email' && !isValidEmail(value)) {
            feedbackElement.textContent = 'Некорректный email';
            feedbackElement.style.color = 'red';
            return;
        }
        
        fetch('/check_availability', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ type: type, value: value }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.available) {
                feedbackElement.textContent = type === 'login' ? 'Логин доступен' : 'Email доступен';
                feedbackElement.style.color = 'green';
            } else {
                feedbackElement.textContent = type === 'login' ? 'Логин уже занят' : 'Email уже занят';
                feedbackElement.style.color = 'red';
            }
        })
        .catch(error => {
            console.error('Ошибка проверки:', error);
            feedbackElement.textContent = 'Ошибка проверки';
            feedbackElement.style.color = 'red';
        });
    }
    
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
});