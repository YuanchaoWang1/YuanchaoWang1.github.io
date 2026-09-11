(() => {
  const dialog = document.querySelector('#diagram-lightbox');
  if (!dialog || typeof dialog.showModal !== 'function') return;

  const fullImage = dialog.querySelector('.diagram-lightbox-image');
  const closeButton = dialog.querySelector('.diagram-lightbox-close');
  let trigger = null;

  document.querySelectorAll('.diagram-image-link').forEach((link) => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      trigger = link;
      const preview = link.querySelector('.diagram');
      fullImage.src = link.href;
      fullImage.alt = preview ? preview.alt : '';
      dialog.showModal();
    });
  });

  closeButton.addEventListener('click', () => dialog.close());

  dialog.addEventListener('close', () => {
    fullImage.removeAttribute('src');
    if (trigger) trigger.focus({ preventScroll: true });
  });
})();
