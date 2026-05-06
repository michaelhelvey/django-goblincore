// see: https://vite.dev/guide/backend-integration
import "vite/modulepreload-polyfill";
import "../css/globals.css";

const themeToNameMap: Record<Theme, string> = {
  light: "Light",
  dark: "Dark",
};

type Theme = "light" | "dark";

function loadTheme(): Theme {
  const savedTheme = localStorage.getItem("theme") as Theme | null;
  return savedTheme ?? "light";
}

function setTheme(themeName: Theme): void {
  localStorage.setItem("theme", themeName);
  document.documentElement.setAttribute("data-theme", themeName);
  updateThemeDisplay(themeName);
}

function updateThemeDisplay(currentTheme: Theme): void {
  const themeNameEl = document.getElementById("current-theme-name");
  if (themeNameEl) {
    themeNameEl.textContent = themeToNameMap[currentTheme];
  }
}

// Update theme display on page load (theme already set by inline script)
document.addEventListener("DOMContentLoaded", () => {
  const theme = loadTheme();
  setTheme(theme);
  updateThemeDisplay(theme);
});

// Make setTheme available globally for onclick handlers
declare global {
  interface Window {
    setTheme: (themeName: Theme) => void;
  }
}

window.setTheme = setTheme;
