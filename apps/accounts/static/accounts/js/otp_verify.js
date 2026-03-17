document.addEventListener("DOMContentLoaded", function () {
  const inputs = document.querySelectorAll(".otp-input input");
  const otp_hidden = document.getElementById("otp");
  const form = document.getElementById("input-form");
  const btn = document.getElementById("verify-btn");
  const otpInputContainer = document.getElementById("otp-input");
  let errorMsg = document.getElementById("otp-error");

  
  if (!errorMsg) {
    errorMsg = document.createElement("p");
    errorMsg.id = "otp-error";
    errorMsg.className = "text-danger mt-2";
    errorMsg.style.display = "none";
    otpInputContainer.parentNode.insertBefore(errorMsg, otpInputContainer.nextSibling);
  }

  window.addEventListener("load", () => {
    inputs.forEach((input) => input.classList.remove("border-danger"));
    const isFormReloads = sessionStorage.getItem("otp_form_submitted");
    if (!isFormReloads) {
      document.querySelectorAll(".server-error").forEach((msg) => msg.style.display = "none");
    } else {
      sessionStorage.removeItem("otp_form_submitted");
      inputs.forEach((input) => input.classList.add("border-danger"));
    }
  });

  inputs.forEach((input, index) => {
    input.addEventListener("input", () => {
      if (input.value && index < inputs.length - 1) {
        inputs[index + 1].focus();
      }
      update_otp();

      errorMsg.style.display = "none";
      inputs.forEach((inp) => inp.classList.remove("border-danger"));
      document.querySelectorAll(".server-error").forEach((msg) => msg.style.display = "none");
    });

    input.addEventListener("keydown", (e) => {
      if (e.key === "Backspace" && !input.value && index > 0) {
        inputs[index - 1].focus();
      }
      update_otp();
    });
  });

  function update_otp() {
    let otp = "";
    inputs.forEach((i) => (otp += i.value));
    otp_hidden.value = otp;
  }

  form.addEventListener("submit", (e) => {
    const otp = otp_hidden.value.trim();

    if (!otp || otp.length !== 6) {
      e.preventDefault(); 
      errorMsg.textContent = "Please enter a valid 6-digit OTP";
      errorMsg.style.display = "block";
      inputs.forEach((input) => input.classList.add("border-danger"));
      inputs[0].focus();
      return false; 
    } 


    sessionStorage.setItem("otp_form_submitted", "true");
    btn.disabled = true;
    btn.innerText = "verifying...";
  });

  // Resend Timer logic
  const resendBtn = document.getElementById("resend-btn");
  let timer = null;
  let timeLeft = 30;

  function startResendTimer() {
    timeLeft = 30;
    resendBtn.disabled = true;
    resendBtn.innerText = `Resend OTP (${timeLeft}s)`;
    if (timer) clearInterval(timer);
    timer = setInterval(() => {
      timeLeft--;
      resendBtn.innerText = `Resend OTP (${timeLeft}s)`;
      if (timeLeft <= 0) {
        clearInterval(timer);
        resendBtn.innerText = "Resend OTP";
        resendBtn.disabled = false;
      }
    }, 1000);
  }

  startResendTimer();

  resendBtn.addEventListener("click", () => {
    if (resendBtn.disabled) return;
    window.location.href = resendBtn.dataset.url;
  });
});