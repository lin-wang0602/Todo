function validatePassword(){
    const password = document.getElementById('new_password').value;
    //regular expression for password
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+={}[\]\|:;"'<>,.?/~`]).{8,}$/;
    if (!regex.test(password)){
      alert("Password must have at least 8 charaters, including digits, uppercase,lowercase , and at least one special charater ")
      return false;
    }
    return true;
    }
    document.getElementById('change_password').addEventListener("submit",(evt) => {
      if(!validatePassword()){
      evt.preventDefault();
    }
    })

function togglePasswordVisibility() {
      const passwordField = document.getElementById("new_password");
      if (passwordField.type === "password") {
        passwordField.type = "text";
      } else {
        passwordField.type = "password";
      }
    }
