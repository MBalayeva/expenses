const usernameField = document.getElementById("usernameField");
const usernameCheckWrapper = document.getElementById("username-check-wrapper");
const usernameErrorWrapper = document.getElementById("username-error-wrapper");

const emailField = document.getElementById("emailField");
const emailErrorWrapper = document.getElementById("email-error-wrapper");

const registerBtn = document.getElementById("register-submit-btn");


usernameField.addEventListener("keyup", (e) => {
  const username = e.target.value;

  usernameField.classList.remove("is-invalid");
  usernameCheckWrapper.classList.remove("d-none");
  usernameErrorWrapper.classList.add("d-none");

  usernameCheckWrapper.innerHTML = `Checking ${username} ...`;

  if (username.length > 0) {
    $.ajax({
      type: "post",
      url: "/authentication/username-validation/",
      data: {
        username: username,
      },
      success: (res) => {
        usernameCheckWrapper.classList.add("d-none");
        registerBtn.disabled = false;
      },
      error: (jqXHR, errorThrown, textStatus) => {
        usernameCheckWrapper.classList.add("d-none");
        usernameField.classList.add("is-invalid");
        usernameErrorWrapper.classList.remove("d-none");
        registerBtn.disabled = true;
        usernameErrorWrapper.innerHTML = `<p>${jqXHR.responseJSON.username_error}</p>`;
      },
    });
  }
});

emailField.addEventListener("keyup", (e) => {
  const email = e.target.value;

  emailField.classList.remove("is-invalid");
  emailErrorWrapper.classList.add("d-none");

  if (email.length > 0) {
    $.ajax({
      type: "post",
      url: "/authentication/email-validation/",
      data: {
        email: email,
      },
      success: (res) => {
        registerBtn.disabled = false;
      },
      error: (jqXHR, errorThrown, textStatus) => {
        emailField.classList.add("is-invalid");
        emailErrorWrapper.classList.remove("d-none");
        registerBtn.disabled = true;
        emailErrorWrapper.innerHTML = `<p>${jqXHR.responseJSON.email_error}</p>`;
      },
    });
  }
});
