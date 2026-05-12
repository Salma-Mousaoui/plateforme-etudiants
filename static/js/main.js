/* EtudiantES — main.js */

function dismissToast(el) {
  if (!el || el.classList.contains('hiding')) return;
  el.classList.add('hiding');
  el.addEventListener('transitionend', function handler() {
    el.removeEventListener('transitionend', handler);
    if (el.parentNode) el.parentNode.removeChild(el);
  });
}

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.elan-toast').forEach(function (toast) {
    toast.addEventListener('dismiss', function () { dismissToast(toast); });
    setTimeout(function () { dismissToast(toast); }, 4000);
  });
});
