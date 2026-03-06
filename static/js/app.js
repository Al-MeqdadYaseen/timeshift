// Core JS

// Timeshift app JavaScript

// Prevent duplicate saves
document.addEventListener("DOMContentLoaded", function () {
  // Find all save forms
  document.querySelectorAll(".save-form").forEach((form) => {
    form.addEventListener("submit", function () {
      const button = this.querySelector(".save-button");
      if (button) {
        button.disabled = true;
        button.textContent = "Saving...";
      }
    });
  });

  // Slider display updates
  const velocitySlider = document.getElementById("velocity-slider");
  const velocityDisplay = document.getElementById("velocityDisplay");

  if (velocitySlider && velocityDisplay) {
    velocitySlider.addEventListener("input", function () {
      velocityDisplay.value = this.value;
    });
  }
});

console.log("Timeshift loaded");

// AI helped me with preventing duplicate saves (frontend) and updating the display value of the velocity slider
