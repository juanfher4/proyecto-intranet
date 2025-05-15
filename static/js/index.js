
/* datatable-clientes */
let dataTable;
let dataTableIsInitialized = false;
 
const dataTableOptions = {
  columnDefs: [
    { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6, 7, 8] },
    { orderable: false, targets: [8] },
    { searchable: false, targets: [8] },
  ],
}

const initDataTable = async () => {
  if (dataTableIsInitialized) {
    dataTable.destroy();
  }

  await listaClientes();

  dataTable = $("#datatable-clientes").DataTable(dataTableOptions);

  dataTableIsInitialized = true;
};

const listaClientes = async () => {
  try {
    const response = await fetch(
      "http://127.0.0.1:8000/productos/clientes/json"
    );
    const data = await response.json();
    console.log(data);

    let content = ``;
    data.clients.forEach((cliente, index) => {
      content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${cliente.nombre}</td>
                    <td>${cliente.comercial__nombre}</td>
                    <td>${cliente.telefono}</td>
                    <td>${cliente.correo}</td>
                    <td>${cliente.ciudad}</td>
                    <td>${cliente.fecha_contacto}</td>
                    <td>${cliente.via_entrada}</td>
                    <td>
                        <a href="{% url 'productos:edit_cliente' cliente.id_cliente %}" class="btn btn-sm btn-primary"><i class="fa-solid fa-pencil"></i></a>
                    </td>
                </tr>
            `;
    });
    let tableBody_clientes = document.getElementById("tableBody_clientes");
    tableBody_clientes.innerHTML = content;
  } catch (ex) {
    console.log(ex);
  }
};

window.addEventListener("load", async () => {
  await initDataTable();
});
