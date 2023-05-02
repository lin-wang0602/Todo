const categoryFilter = document.getElementById('category_filter');
const todoRows = document.querySelectorAll('.todo-row');
categoryFilter.addEventListener('change', () => {

  const selectedCategory = categoryFilter.value;
  todoRows.forEach((row) => {
    const id = row.id
    const targetCategory = document.querySelector(`#category-${id}`)
  if (selectedCategory === '' ){
      row.style.display = 'table-row';
      }
  else {
    if(targetCategory.dataset.categoryname === (selectedCategory)){
      row.style.display = 'table-row';
    }else{
      row.style.display = 'none';
    }

  };
});

});
