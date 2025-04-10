document.addEventListener('DOMContentLoaded', function() {
    // Делегирование событий для кнопок
    document.addEventListener('click', function(e) {
        const target = e.target;
        
        // Обработка кнопок открытия модальных окон
        if (target.matches('[data-modal]') && !target.matches('.close')) {
            const modalId = target.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.style.display = 'block';
                document.body.style.overflow = 'hidden';
            }
            e.preventDefault();
            return;
        }
        
        // Обработка кнопок закрытия модальных окон
        if (target.matches('.close')) {
            const modalId = target.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
            e.preventDefault();
            return;
        }
        
        // Обработка кнопки "Добавить игру"
        if (target.matches('#toggleAddGameForm')) {
            const action = target.getAttribute('data-action');
            if (action === 'toggle-form') {
                const form = document.querySelector('.add-game-form');
                if (form) {
                    form.style.display = form.style.display === 'none' ? 'block' : 'none';
                    if (form.style.display === 'block') {
                        form.scrollIntoView({ behavior: 'smooth' });
                    }
                }
            } else if (action === 'show-login') {
                const loginModal = document.getElementById('loginModal');
                if (loginModal) {
                    loginModal.style.display = 'block';
                    document.body.style.overflow = 'hidden';
                }
            }
            e.preventDefault();
            return;
        }
        
        // Обработка клика вне модальных окон
        const modals = document.querySelectorAll('.modal');
        modals.forEach(function(modal) {
            if (target === modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
        
        // Обработка клика вне формы добавления игры
        const addGameForm = document.querySelector('.add-game-form');
        if (addGameForm && addGameForm.style.display === 'block' && 
            !addGameForm.contains(target) && 
            !target.matches('#toggleAddGameForm')) {
            addGameForm.style.display = 'none';
        }
    });

    // Обработка flash-сообщений
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.style.display = 'none';
            }, 1000); 
        }, 5000);
    });

    // Проверка доступности логина и email
    const loginInput = document.getElementById('login');
    const emailInput = document.getElementById('pochta');
    const loginFeedback = document.createElement('div');
    const emailFeedback = document.createElement('div');    
   
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