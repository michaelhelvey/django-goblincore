import "../css/globals.css";

console.log("I am a typescript file executing after being pre-processed by vite!");

// Theme Management
type Theme = "light" | "dark" | "cupcake" | "bumblebee" | "emerald" | "corporate" | "synthwave";

function loadTheme(): Theme {
  const savedTheme = localStorage.getItem("theme") as Theme | null;
  return savedTheme || "light";
}

function setTheme(themeName: Theme): void {
  localStorage.setItem("theme", themeName);
  document.documentElement.setAttribute("data-theme", themeName);
  updateThemeDisplay(themeName);
}

function updateThemeDisplay(currentTheme: Theme): void {
  const themeNameEl = document.getElementById("current-theme-name");
  if (themeNameEl) {
    themeNameEl.textContent = currentTheme.charAt(0).toUpperCase() + currentTheme.slice(1);
  }

  // Update checkmarks on theme options
  document.querySelectorAll(".theme-option").forEach((option) => {
    const themeName = option.getAttribute("data-theme");
    if (themeName === currentTheme) {
      option.classList.add("active");
    } else {
      option.classList.remove("active");
    }
  });
}

// Update theme display on page load (theme already set by inline script)
document.addEventListener("DOMContentLoaded", () => {
  const theme = loadTheme();
  updateThemeDisplay(theme);
});

// Make setTheme available globally for onclick handlers
declare global {
  interface Window {
    setTheme: (themeName: Theme) => void;
  }
}

window.setTheme = setTheme;
