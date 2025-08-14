(() => {
  const KEY = 'theme';
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  const set = t => { document.documentElement.setAttribute('data-theme', t); localStorage.setItem(KEY, t); };

  const saved = localStorage.getItem(KEY);
  set(saved || (media.matches ? 'dark' : 'light'));
  if (media.addEventListener) media.addEventListener('change', e => { if (!localStorage.getItem(KEY)) set(e.matches ? 'dark' : 'light'); });

  document.addEventListener('click', e => {
    const btn = e.target.closest('#theme-toggle');
    if (!btn) return;
    set(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  });
})();