window.addEventListener("DOMContentLoaded", function () {
  const filterInput = document.getElementById("filter");
  const type = document.getElementById("type").innerText;

  filterInput.onkeyup = function () {
    const value = this.value.toLowerCase();
    const arr = document.getElementsByClassName("item-card");

    if (!value.length) {
      for (const e of arr) {
        e.classList.remove("none");
      }
      return;
    }

    switch (type) {
      case "Login Credentials":
        for (const e of arr) {
          if (
            !e.dataset.name.toLowerCase().includes(value) &&
            !e.dataset.service.toLowerCase().includes(value)
          ) {
            e.classList.add("none");
          } else {
            e.classList.remove("none");
          }
        }
        break;

      case "Payment Cards":
        for (const e of arr) {
          if (
            !e.dataset.name.toLowerCase().includes(value) &&
            !e.dataset.number.toLowerCase().includes(value) &&
            !e.dataset.bank.toLowerCase().includes(value)
          ) {
            e.classList.add("none");
          } else {
            e.classList.remove("none");
          }
        }
        break;

      case "Security Notes":
        for (const e of arr) {
          if (!e.dataset.title.toLowerCase().includes(value)) {
            e.classList.add("none");
          } else {
            e.classList.remove("none");
          }
        }
        break;
    }
  };
});
