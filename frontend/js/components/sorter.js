document.querySelectorAll('.sort-by button').forEach((button) => {
  button.addEventListener('click', (e) => {
    const parentContainer = e.currentTarget.parentElement;
    const list = parentContainer.querySelector('.sort-list');
    if (list.classList.contains('d-none')) {
      list.classList.remove('d-none');
      parentContainer.querySelector('.click-area').classList.remove('d-none');
    } else {
      list.classList.add('d-none');
      parentContainer.querySelector('.click-area').classList.add('d-none');
    }
  });
});

document.querySelectorAll('.sort-by .click-area').forEach((click) => {
  click.addEventListener('click', (e) => {
    document.querySelectorAll('.sort-by .sort-list').forEach((list) => {
      list.classList.add('d-none');
    });
    e.currentTarget.classList.add('d-none');
  });
});
