document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.toggle-submenu');
  const submenu = document.querySelector('.submenu');

  toggle.addEventListener('click', (e) => {
    e.preventDefault();
    submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
  });

  // Opcional: cerrar si se hace clic fuera
  document.addEventListener('click', (e) => {
    if (!toggle.contains(e.target) && !submenu.contains(e.target)) {
      submenu.style.display = 'none';
    }
  });
});
