window.addEventListener("DOMContentLoaded", function () {
  document.getElementById("reveal-wordlist").addEventListener("click", () => {
    document.querySelectorAll(".wordlist-word").forEach((e) => {
      e.classList.remove("blur");
    });
  });
});
