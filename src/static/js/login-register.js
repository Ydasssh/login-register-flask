function validationRegister() {
  const user = document.FormfillRegister.Username.value;
  const email = document.FormfillRegister.Email.value;
  const pass = document.FormfillRegister.Password.value;
  const confirmPass = document.FormfillRegister.CPassword.value;
  const result = document.getElementById('resultado');


  if (user === "") {
    text = "Enter Username";
    alert2(text, 'error')
    return false;
  } else if (user.length < 6) {
    text ="At least six letters";
    alert2(text, 'error')
    return false;
  } else if (email === "") {
    text = "Enter your Email";
    alert2(text, 'error')
    return false;
  }else if(!email == '@'){
    text = "Wrong email, @ is required";
    alert2(text, 'error')
    return false;
  } else if (pass === "") {
    text = "Enter your password";
    alert2(text, 'error')
    return false;
  } else if (confirmPass === "") {
    text = "Enter confirm password";
    alert2(text, 'error')
    return false;
  } else if (pass.length < 6) {
    text = "Password must be 6 characters";
    alert2(text, 'error')
    return false;
  } else if (confirmPass !== pass) {
    text = "Password doesn't match";
    alert2(text, 'error')
    return false;
  } else {
    return true;
  }
}


function validationLogin() {
  const pass = document.FormfillLogin.Password.value;
  const email = document.FormfillLogin.Email.value;

  if (email === "") {
    alert2('Ingresar correo','error')
  }else if(email.indexOf('@') === -1 || email.indexOf('.com') === -1) {
    alert2('Ingresar un correo válido', 'error');
  } 
  else if (pass === "") {
    alert2('Ingresar contraseña','error')
  }else{

    const formData = new FormData();
    formData.append('correo', email);
    formData.append('contraseña', pass);

    fetch('/login', {
      method: 'POST',
      body: formData
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        return response.json().then(data => {
          throw new Error(data.error || 'Ha ocurrido un error en la solicitud.');
        });
      }
    })
    .then(data => {
      alert2(data.success, 'success');
      setTimeout(function() {
        location.reload();
      }, 3000);
    })
    .catch(error => {
      // Manejar el error en caso de respuesta no exitosa
      alert2(data.error, 'error');
      console.error('Error al obtener los datos:', error);
    });
  }

}
