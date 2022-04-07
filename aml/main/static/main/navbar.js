const COLORS = {
  "--primary": {
    dark: "black",
    light: "white",
  },
  "--secondary": {
    dark: "white",
    light: "black",
  },
  "--white-transparent-dark": {
    dark: "rgba(0, 0, 0, 0.6)",
    light: "rgba(255, 255, 255, 0.6)",
  },
  "--gray-transparent-dark": {
    dark: "rgba(255, 255, 255, 0.8)",
    light: "rgba(0, 0, 0, 0.8)",
  },
  "--gray-transparent": {
    dark: "rgba(255, 255, 255, 0.1)",
    light: "rgba(0, 0, 0, 0.1)",
  },
  "--gray-light": {
    dark: "#161616",
    light: "#f7f7f7",
  },
};

/**
 * Changes CSS variables based on a colors object and the dark them state
 * @param {object} colors
 * @param {boolean} dark
 * @returns {void}
 */
function changeCssVariables(colors, dark = false) {
  // On transforme le booleen en string "dark" || "light"
  const theme = dark ? "dark" : "light";

  //   Pour chaque variable (clé) dans l'objet colors
  for (const variable_name in colors) {
    // On récupère les deux couleurs de la variable
    const variable = colors[variable_name];
    // On récupère la bonne couleur en fonction du thème
    const color = variable[theme];

    // On définis la variable dans notre page HTML
    document.documentElement.style.setProperty(variable_name, color);
  }
}

/**
 * Add style (property: value) on every element in the DOM
 * @param {string} property
 * @param {string} value
 * @returns {void}
 */
function addStyleToAllElements(property, value) {
  const elements = document.querySelectorAll("*");

  for (const element of elements) {
    if (
      window.getComputedStyle(element).getPropertyValue(property) !==
      "all 0s ease 0s"
    )
      continue;
    element.style.setProperty(property, value);
  }
}

function handleDarkTheme() {
  // On récupère l'element de type checkbox
  const checkbox = document.getElementById("darkmode");

  // On récupère le status du mode sombre dans le localStorage
  // Si il n'y a pas de valeur on dit que c'est égal a false
  const darkMode = localStorage.darkMode === "true" || false;

  // On définis le status de la checkbox
  checkbox.checked = darkMode;

  //   On change les variables CSS
  changeCssVariables(COLORS, darkMode);

  //   On ajoute la transition sur tout les elements
  setTimeout(() => {
    addStyleToAllElements(
      "transition",
      "background-color ease-in 0.5s, color ease 0.5s"
    );
  }, 0);

  // Quand on clique sur la checkbox
  checkbox.onclick = () => {
    // On change la valeur du mode sombre dans le localStorage
    localStorage.darkMode = checkbox.checked;
    // On change les variables CSS
    changeCssVariables(COLORS, checkbox.checked);
  };
}

function handleNotifications() {
  const popup_button = document.getElementById("popup-btn");
  const popup = document.getElementById("popup");
  const cards = document.getElementsByClassName("popup__card");

  if (cards.length === 0) {
    popup_button.remove();
    popup.remove();
  }

  popup_button.onclick = () => {
    popup.classList.toggle("popup--show");
  };

  // Quand on clique sur la page (n'importe où)
  document.onclick = (event) => {
    // On récupère l'élément sur lequel on a cliqué
    const element_on_cursor = document.elementFromPoint(
      event.clientX,
      event.clientY
    );
    
    // Si on a cliqué sur la popup on ne fais rien
    if (element_on_cursor.id === "popup-btn__icon" || element_on_cursor.className.startsWith("popup")) return;
    
    // Si on n'a pas cliqué sur la popup ET que la popup est active, on la cache
    if (popup.classList.contains("popup--show")) {
      popup.classList.remove("popup--show");
    }
  };
}

handleDarkTheme();
handleNotifications();
