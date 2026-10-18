/**
 * Herbalist AI - Interactive Platform Client
 */
console.log("%c🌿 Herbalist AI Research Platform v2.0", "color:#2ee6a8;font-weight:700;font-size:14px;");

document.addEventListener("DOMContentLoaded", function() {
  // Global image error fallback for any broken images
  document.querySelectorAll("img.hx-photo, img.plant-image").forEach(img => {
    img.addEventListener("error", function() {
      console.warn("Image load failed, applying graceful fallback:", this.src);
      if (!this.getAttribute("data-fallback-applied")) {
        this.setAttribute("data-fallback-applied", "true");
        this.src = "/static/images/landing.png";
      }
    });
  });

  // Table filtering on plants browser if present
  const searchInput = document.getElementById("plantSearchInput");
  if (searchInput) {
    searchInput.addEventListener("input", function(e) {
      const q = e.target.value.toLowerCase();
      document.querySelectorAll(".hx-table tbody tr").forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(q) ? "" : "none";
      });
    });
  }
});
