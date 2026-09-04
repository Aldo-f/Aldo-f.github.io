document.addEventListener('DOMContentLoaded', () => {
  const search = document.getElementById('search');
  if (search) {
    search.addEventListener('click', async () => {
      const { default: pagefind } = await import('/pagefind-ui/pagefind-ui.js');
      const result = await pagefind();
      result.show();
    });
  }
});