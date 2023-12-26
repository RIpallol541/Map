// Получаем ссылку на элемент мяча
var ball = document.getElementById('ball');

// Начальные координаты мяча
var x = 0;
var y = 0;

// Функция для обновления позиции мяча
function updateBallPosition() {
    // Изменяем координаты мяча
    x += 5;  // Изменение по оси X
    y = Math.sin(x / 10) * 50 + 100;  // Изменение по оси Y (в примере - синусоида)

    // Устанавливаем новые координаты мяча
    ball.style.left = x + 'px';
    ball.style.top = y + 'px';

    // Рекурсивный вызов функции для создания анимации
    requestAnimationFrame(updateBallPosition);
}

// Запускаем анимацию
updateBallPosition();