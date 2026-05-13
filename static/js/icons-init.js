window.addEventListener("DOMContentLoaded", function () {
  if (window.lucide) {
    window.lucide.createIcons();
  }
});
document.body.addEventListener("htmx:afterSwap", function () {
  if (window.lucide) {
    window.lucide.createIcons();
  }
});
