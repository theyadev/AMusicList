const popup_button = document.getElementById("popup-btn")
const popup = document.getElementById("popup")

if (popup.getElementsByClassName("popup__card").length === 0) popup_button.style.display = "none" 

popup_button.onclick = () => {
    popup.classList.toggle("popup--hidden")
}