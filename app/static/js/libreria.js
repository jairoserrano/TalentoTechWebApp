// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
  "use strict";

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll(".needs-validation");

  // Loop over them and prevent submission
  Array.from(forms).forEach((form) => {
    form.addEventListener(
      "submit",
      (event) => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        form.classList.add("was-validated");
      },
      false
    );
  });
})();

// Aquí puedes agregar tu código JavaScript personalizado
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("galletas").addEventListener("click", function () {
    fetch("/galletas")
      .then((response) => response.text())
      .then((data) => {
        document.querySelector("main").innerHTML = data;
      })
      .catch((error) => console.error("Error:", error));
  });

  document.getElementById("perfil").addEventListener("click", function () {
    fetch("/perfil")
      .then((response) => response.text())
      .then((data) => {
        document.querySelector("main").innerHTML = data;
      })
      .catch((error) => console.error("Error:", error));
  });
});
