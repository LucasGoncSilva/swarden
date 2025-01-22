window.addEventListener("DOMContentLoaded", () => {
  const revealBtnArr = document.getElementsByClassName('reveal')
  const copyBtnArr = document.getElementsByClassName('copy')


  for (const btn of revealBtnArr) {
    btn.onclick = function () {
      const keyElem = this.parentElement.previousSibling.previousSibling
      keyElem.innerText = keyElem.innerText == '*****' ? keyElem.dataset.value : '*****'
    }
  }

  for (const btn of copyBtnArr) {
    btn.onclick = function () {
      const keyElem = this.parentElement.previousSibling.previousSibling
      navigator.clipboard.writeText(keyElem.dataset.value)
    }
  }

})