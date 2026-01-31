import "../css/globals.css";

const themeToNameMap: Record<Theme, string> = {
  cupcake: "Light",
  dark: "Dark",
};

type Theme = "cupcake" | "dark";

function loadTheme(): Theme {
  const savedTheme = localStorage.getItem("theme") as Theme | null;
  return savedTheme ?? "cupcake";
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
