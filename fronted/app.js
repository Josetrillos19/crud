function consulta_general() {
  let url = "http://127.0.0.1:5000/";
  fetch(url)
      .then(response => response.json())
      .then(data => visualizar(data))
      .catch(error => console.log(error));

  const visualizar = (data) => {
      console.log(data);
      let b = '';
      for (let i = 0; i < data.baul.length; i++) {
          console.log(data.baul[i].Plataforma);
          console.log(data.baul[i].usuario);
          console.log(data.baul[i].clave);
          b += `<tr>
                  <td>${data.baul[i].id_baul}</td>
                  <td>${data.baul[i].Plataforma}</td>
                  <td>${data.baul[i].usuario}</td>
                  <td>${data.baul[i].clave}</td>
                  <td>
                      <button type='button' class='btn btn-info' onclick="location.href='edit.html?variable1=${data.baul[i].id_baul}'">
                          <img src='img/editar.png' height='30' width='30'/>
                      </button>
                      <button type='button' class='btn btn-warning' onclick="eliminar(${data.baul[i].id_baul})">
                          <img src='img/borrar.png' height='30' width='30'/>
                      </button>
                  </td>
                </tr>`;
      }
      document.getElementById('data').innerHTML = b;
  };
}

function eliminar(id) {
  let url = "http://127.0.0.1:5000/eliminar/" + id;
  fetch(url, {
      method: 'DELETE',
  })
  .then(response => response.json())
  .then(res => visualizar(res))
  .catch(error => console.error("Error:", error));

  const visualizar = (res) => {
      swal("Mensaje", "Registro " + res.mensaje + " exitosamente", "success")
      .then(() => {
          window.location.reload();
      });
  };
}

function registrar() {
  let url = "http://127.0.0.1:5000/registro/";
  let plata = document.getElementById("plataforma").value;
  let usua = document.getElementById("usuario").value;
  let clave = document.getElementById("clave").value;
  let data = {
      "plataforma": plata,
      "usuario": usua,
      "clave": clave
  };
  console.log(data);

  fetch(url, {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
          "Content-Type": "application/json",
      },
  })
  .then((res) => res.json())
  .then((response) => visualizar(response))
  .catch((error) => console.error("Error:", error));

  const visualizar = (response) => {
      console.log("Success:", response);
      if (response.mensaje === "Error") {
          swal("Mensaje", "Error en el registro", "error");
      } else {
          swal("Mensaje", "Registro agregado exitosamente", "success");
      }
  };
}

function consulta_individual(id) {
  let url = "http://127.0.0.1:5000/consulta_individual/" + id;
  fetch(url)
      .then(response => response.json())
      .then(data => visualizar(data))
      .catch(error => console.log(error));

  const visualizar = (data) => {
      console.log(data);
      document.getElementById("plataforma").value = data.baul.Plataforma;
      document.getElementById("usuario").value = data.baul.usuario;
      document.getElementById("clave").value = data.baul.clave;
  };
}

function modificar(id) {
  let url = "http://127.0.0.1:5000/actualizar/" + id;
  let plat = document.getElementById("plataforma").value;
  let usua = document.getElementById("usuario").value;
  let clav = document.getElementById("clave").value;
  let data = {
      "plataforma": plat,
      "usuario": usua,
      "clave": clav
  };

  console.log(data);
  fetch(url, {
      method: "PUT",
      body: JSON.stringify(data),
      headers: {
          "Content-Type": "application/json",
      },
  })
  .then((res) => res.json())
  .then((response) => visualizar(response))
  .catch((error) => console.error("Error:", error));

  const visualizar = (response) => {
      console.log("Success:", response);
      if (response.mensaje === "Error") {
          swal("Mensaje", "Error en la actualización", "error");
      } 
      else {
          swal("Mensaje", "Registro actualizado exitosamente", "success");
      }
  };
}
