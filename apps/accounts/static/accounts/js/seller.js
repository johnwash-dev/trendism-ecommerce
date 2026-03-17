document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("sellerForm");
    const shopName = document.getElementById("shopName");
    const gstNumber = document.getElementById("gstNumber");
    const address = document.getElementById("address");

    if (!form) return;

    function showError(input, message) {
        clearError(input);
        
        const errorMsg = document.createElement("small");
        errorMsg.className = "js-error-msg text-danger d-block mt-1 mb-2";
        errorMsg.style.fontSize = "12px";
        errorMsg.textContent = message;
        
        input.classList.add("is-invalid", "border-danger");
        input.parentElement.appendChild(errorMsg);
    }

    function clearError(input) {
        const parent = input.parentNode;
        const existingError = parent.querySelector(".js-error-msg");
        if (existingError) {
            existingError.remove();
        }
        input.classList.remove("is-invalid", "border-danger");
    }

    form.addEventListener("submit", function (e) {
        let isValid = true;


        if (shopName.value.trim() === "") {
            showError(shopName, "Shop name should not be empty");
            isValid = false;
        } else if (shopName.value.trim().length < 3) {
            showError(shopName, "Shop name is too short (min 3 chars)");
            isValid = false;
        }

        const gstRegex = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/;
        if (gstNumber.value.trim() === "") {
            showError(gstNumber, "GST number should not be empty");
            isValid = false;
        } else if (!gstRegex.test(gstNumber.value.trim().toUpperCase())) {
            showError(gstNumber, "Enter a valid 15-digit GST number");
            isValid = false;
        }

        if (address.value.trim() === "") {
            showError(address, "Address field should not be empty");
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault(); 
        }
    });

    [shopName, gstNumber, address].forEach(input => {
        input.addEventListener("input", () => clearError(input));
    });
});