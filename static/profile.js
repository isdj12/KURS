document.addEventListener('DOMContentLoaded', function() {
    // Обработка загрузки аватара
    const avatarInput = document.getElementById('avatar-input');
    const avatarPreview = document.getElementById('avatar-preview');
    
    if (avatarInput && avatarPreview) {
        avatarInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    avatarPreview.src = e.target.result;
                    // Здесь можно добавить AJAX-запрос для сохранения аватара
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Обработка загрузки дополнительных изображений
    const additionalImageInputs = document.querySelectorAll('.additional-image-input');
    const additionalImagePreviews = document.querySelectorAll('.additional-image');
    
    additionalImageInputs.forEach((input, index) => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    additionalImagePreviews[index].src = e.target.result;
                    // Здесь можно добавить AJAX-запрос для сохранения изображения
                }
                reader.readAsDataURL(file);
            }
        });
    });

    // Обработка нажатия на кнопки изменения изображений
    const changeImageBtns = document.querySelectorAll('.change-image-btn');
    changeImageBtns.forEach((btn, index) => {
        btn.addEventListener('click', function() {
            additionalImageInputs[index].click();
        });
    });

    // Обработка нажатия на кнопку изменения аватара
    const changeAvatarBtn = document.querySelector('.change-avatar-btn');
    if (changeAvatarBtn) {
        changeAvatarBtn.addEventListener('click', function() {
            avatarInput.click();
        });
    }
}); 