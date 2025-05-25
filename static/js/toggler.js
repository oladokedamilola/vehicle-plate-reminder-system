document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('darkModeToggle');
  const darkModeHref = '/static/css/darkmode.css';  // Adjust paths as needed
  const lightModeHref = '/static/css/lightmode.css';
  const themeLinkId = 'theme-css';

  // Create or get the <link> element that loads the theme CSS
  let themeLink = document.getElementById(themeLinkId);
  if (!themeLink) {
    themeLink = document.createElement('link');
    themeLink.rel = 'stylesheet';
    themeLink.id = themeLinkId;
    document.head.appendChild(themeLink);
  }

  // Load saved theme from localStorage or default to light mode
  const savedTheme = localStorage.getItem('theme') || 'light';
  themeLink.href = savedTheme === 'dark' ? darkModeHref : lightModeHref;

  // Set toggle checkbox based on saved theme
  toggle.checked = savedTheme === 'dark';

  // Toggle event handler
  toggle.addEventListener('change', () => {
    if (toggle.checked) {
      themeLink.href = darkModeHref;
      localStorage.setItem('theme', 'dark');
    } else {
      themeLink.href = lightModeHref;
      localStorage.setItem('theme', 'light');
    }
  });
});
