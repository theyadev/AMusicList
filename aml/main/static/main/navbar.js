const popup_button = document.getElementById("popup-btn")
const popup = document.getElementById("popup")

if (popup.getElementsByClassName("popup__card").length === 0) popup_button.style.display = "none" 

popup_button.onclick = () => {
    popup.classList.toggle("popup--show")
}

const colors = {
    "--primary": {
        dark: "black",
        light: "white"
    },
    "--secondary": {
        dark: "gray",
        light: "blue"
    }
}

const checkbox = document.getElementById("darkmode")
const darkMode = localStorage.darkMode === "true" || false

checkbox.checked = darkMode 

changeRootVariable(darkMode)

checkbox.onclick = () => {
    localStorage.darkMode = checkbox.checked
    changeRootVariable(checkbox.checked)
}

function changeRootVariable(dark = false) {
    const theme = dark ? "dark" : "light"

    for (const key in colors) {
        document.documentElement.style.setProperty(key, colors[key][theme]);
    }
}