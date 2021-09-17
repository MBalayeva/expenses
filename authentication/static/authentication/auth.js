const togglePassword = document.getElementById("toggle-password");
const passwordField = document.getElementById("passwordField");

togglePassword.addEventListener("click", () => {
  if (togglePassword.textContent === "SHOW PASSWORD") {
    togglePassword.textContent = "HIDE PASSWORD";
    passwordField.setAttribute("type", "text");
  } else {
    togglePassword.textContent = "SHOW PASSWORD";
    passwordField.setAttribute("type", "password");
  }
});
