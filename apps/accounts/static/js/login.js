document.addEventListener("DOMContentLoaded", function () {

  const email = document.getElementById("emailInput");
  const form = email.closest("form");
  let errorMsg = null;

  function createErrorElement() {
    if (!errorMsg) {
      errorMsg = document.createElement("p");
      errorMsg.id = "input-error";
      errorMsg.className = "text-danger";
      errorMsg.style.display = "none";
      email.parentNode.insertBefore(errorMsg, email.nextSibling);
    }
  }

  function showError(message) {
    createErrorElement();
    errorMsg.textContent = message;
    errorMsg.style.display = "block";
    email.classList.add("border-danger");
  }

  function clearError() {
    if (errorMsg) {
      errorMsg.textContent = "";
      errorMsg.style.display = "none";
    }
    email.classList.remove("border-danger");
  }

  function isValidEmail(emailValue) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(emailValue);
  }

  email.addEventListener("input", () => {
    clearError();
  });

  form.addEventListener("submit", (e) => {
    const emailValue = email.value.trim();

    if (emailValue === "") {
      e.preventDefault();
      showError("Please enter your email");
      email.focus();
      return;
    }

    if (!isValidEmail(emailValue)) {
      e.preventDefault();
      showError("Please enter a valid email address");
      email.focus();
      return;
    }
  });
});
