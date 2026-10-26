/**
 * JalaRaksha Vanilla JavaScript Client Helper
 * Mobile navigation, clipboard copy, and flash dismissals.
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Menu Toggle
  const toggleBtn = document.querySelector('.mobile-nav-toggle');
  const navMenu = document.querySelector('.nav-menu');

  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', () => {
      const isOpen = navMenu.classList.toggle('is-open');
      toggleBtn.setAttribute('aria-expanded', isOpen);
    });
  }

  // 2. Copy Reference Code to Clipboard
  const copyButtons = document.querySelectorAll('[data-copy-target]');
  copyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-copy-target');
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        const textToCopy = targetEl.innerText || targetEl.value;
        navigator.clipboard.writeText(textToCopy).then(() => {
          const originalText = btn.innerHTML;
          btn.innerHTML = '✓ Copied!';
          btn.classList.add('btn-accent');
          setTimeout(() => {
            btn.innerHTML = originalText;
            btn.classList.remove('btn-accent');
          }, 2000);
        }).catch(() => {
          alert('Could not copy code automatically. Please select and copy manually.');
        });
      }
    });
  });

  // 3. Flash alert dismiss buttons
  const flashCloseButtons = document.querySelectorAll('.flash-close-btn');
  flashCloseButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const alert = btn.closest('.flash-alert');
      if (alert) {
        alert.remove();
      }
    });
  });
});
