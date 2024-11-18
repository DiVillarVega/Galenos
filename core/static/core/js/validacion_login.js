$(document).ready(function() {

   // Agregar método de validación para RUT chileno
   $.validator.addMethod("rutChileno", function(value, element) {

    // Validar que el RUT tenga el formato correcto (8 o 9 dígitos + guión + dígito verificador)
    var rutPattern = /^\d{7,8}-[\dK]$/;
    if (!rutPattern.test(value)) {
        return false;
    }

    // Validar el dígito verificador
    var rutSinGuion = value.replace("-", "");
    var rut = rutSinGuion.slice(0, -1);
    var dv = rutSinGuion.slice(-1);
    var factor = 2;
    var sum = 0;
    for (var i = rut.length - 1; i >= 0; i--) {
        sum += parseInt(rut.charAt(i)) * factor;
        factor = factor === 7 ? 2 : factor + 1;
    }
    var dvCalculado = 11 - (sum % 11);
    dvCalculado = dvCalculado === 11 ? "0" : dvCalculado === 10 ? "K" : dvCalculado.toString();

    return dv === dvCalculado;
  }, "El RUT no es válido (escriba sin puntos y con guión)");


   // Agregar método de validación para correo
   $.validator.addMethod("emailCompleto", function(value, element) {

    // Expresión regular para validar correo electrónico
    var regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z\-0-9]{2,}))$/;

    // Validar correo electrónico con la expresión regular
    return regex.test(value);

  }, 'El formato del correo no es válido');

   // Validar formulario de login
   $('#formulario_login').validate(
    {
      rules: {
        'username': {
          required: true,
          rutChileno: true
        },
        'password': {
          required: true
        }
      },
      messages: {
        'username': {
          required: 'El usuario es un campo obligatorio.',
          rutChileno: 'El RUT no es válido (escriba sin puntos y con guión)'
        },
        'password': {
          required: 'La contraseña es un campo requerido.'
        }
      },
      errorPlacement: function(error, element) {
        error.insertAfter(element); // Inserta el mensaje de error después del elemento
        error.addClass('error-message'); // Aplica una clase al mensaje de error
      },
    }
  );
});