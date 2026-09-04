// Material MkDocs search: Ctrl+K / Cmd+K shortcut
document.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    const searchToggle = document.getElementById('__search');
    if (searchToggle) { searchToggle.click(); }
  }
});
