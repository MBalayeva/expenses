const togglePassword = document.querySelectorAll(".toggle-password");
const passwordField = Array.from(document.querySelectorAll('input[type=password]'))

// togglePassword.addEventListener("click", () => {
//   if (togglePassword.textContent === "SHOW PASSWORD") {
//     togglePassword.textContent = "HIDE PASSWORD";
//     passwordField.setAttribute("type", "text");
//   } else {
//     togglePassword.textContent = "SHOW PASSWORD";
//     passwordField.setAttribute("type", "password");
//   }
// });


togglePassword.forEach(btn=> {
  btn.addEventListener("click", () => {
    if (btn.textContent === "SHOW PASSWORD") {
      btn.textContent = "HIDE PASSWORD";
      passwordField.find(pw => pw.dataset.id === btn.dataset.id).setAttribute("type", "text");
    } else {
      btn.textContent = "SHOW PASSWORD";
      passwordField.find(pw => pw.dataset.id === btn.dataset.id).setAttribute("type", "password");
    }
  });
})