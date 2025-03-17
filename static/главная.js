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