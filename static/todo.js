// delete for all_todos.html
const deleteButtons = document.querySelectorAll('.delete-todo');
// Add a click event listener to each delete button
deleteButtons.forEach(button => {
  button.addEventListener('click', (event) => {
    event.preventDefault();
    const todoListId = button.getAttribute('todo_list_id');
    const todoDescri = button.getAttribute('description');
    const confirmDelete = confirm(`Are you sure you want to delete this todo list : "${todoDescri}"?`);
    if (confirmDelete){
    fetch('/delete_todo/' + todoListId, { method: 'POST' }) // call to the server to delete todo list with given todoListId
      .then(response => {
        if (response.ok) {
          window.location.reload(); // Reload the page if deletion is successful
        } else {
          console.log('An error occurred while deleting the todo list');
        }
      })
      .catch(error => console.error(error));
    }
  });
});

// login for login.html
const login = document.getElementById("login");
const createAccount = document.getElementById("create-account");
const createUserForm = document.getElementById("create-user-form");
const loginForm = document.getElementById("login-form");
const createUserButton = document.getElementById("create-user-button");
const loginButton = document.getElementById("login-button");

createAccount.style.display = "none";
createUserForm.style.display = "none";

createUserButton.addEventListener("click", () => {
  createUserButton.style.backgroundColor = "#4285F4"
  loginButton.style.backgroundColor = "#E0E0E0"
  createAccount.style.display = "block";
  createUserForm.style.display = "block";
  loginForm.style.display = "none";
  login.style.display = "none";
});

loginButton.addEventListener("click", () => {
  loginButton.style.backgroundColor = "#4285F4"
  createUserButton.style.backgroundColor = "#E0E0E0"
  createAccount.style.display = "none";
  createUserForm.style.display = "none";
  loginForm.style.display = "block";
  login.style.display = "block";
});

// contraints for password
function validatePassword(){
const password = document.getElementById('password').value;
//regular expression for password
const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+={}[\]\|:;"'<>,.?/~`]).{8,}$/;
if (!regex.test(password)){
  alert("Password must have at least 8 charaters, including digits, uppercase,lowercase , and at least one special charater ")
  return false;
}
return true;
}
document.getElementById('create-user-form').addEventListener("submit",(evt) => {
  if(!validatePassword()){
  evt.preventDefault();
}
})
