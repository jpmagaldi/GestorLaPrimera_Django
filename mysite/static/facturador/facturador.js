document.addEventListener("DOMContentLoaded", function () {
	
	const BCliente = document.getElementById("BCliente");
	const BProductos = document.getElementById("BProductos");
	const cerrarModalClientes = document.getElementById("CerrarModalClientes");
	const ModalCliente = document.getElementById("ModalCliente");
	const ModalProductos = document.getElementById("ModalProductos");
	const ModalCantidad = document.getElementById("ModalCantidad");
	const ModalPrecio = document.getElementById("ModalPrecio");
	const SearchBar_Client = document.getElementById("SearchBar_Client");
	const SearchBar_Products = document.getElementById("SearchBar_Products");
	const TablaProductos = document.getElementById("tablaProductos");
	const TablaModalProductos = document.getElementById("TablaModalProductos");
	const TablaModalClient = document.getElementById("TablaModalClient");
	const InputCant = document.getElementById("InputCant");
	const InputPrecio = document.getElementById("InputPrecio");
	const BCerrarCant = document.getElementById("BCerrarCant");
	const BCerrarPrec = document.getElementById("BCerrarPrec");
	const Facturacheck = document.getElementById("option1label");
	const Facturacheck1 = document.getElementById("option2label");
	const radio = document.getElementsByName("toggle")
	const urlTemplate = JSON.parse(
		document.getElementById("url-template").textContent
	);

	const regex = /^(?:\d{1,8}|\d{1,8}\.\d{1,4})$/;


	function mostrarAlerta(mensaje) {
		const barra = document.getElementById('alerta-error');
		barra.textContent = mensaje;
		barra.style.display = 'block';

		// Ocultar después de 5 segundos
		setTimeout(() => {
			barra.style.display = 'none';
		}, 5000);
	}

	/* Funciones de ARCA */

	document.querySelector('#modalarca').style.display = 'block';
	fetch(urlTemplate.url_wsaa, {
		headers: {
			'X-Internal-Token': 'token-seguro-123',
			'Content-Type': 'application/json'
		},
	})
		.then(res => res.json())
		.then(data => {
			const estado = document.getElementById('estado-wsaa');
			if (data.err == 0) {
				estado.innerHTML = `<h3 style="color: green">¡Listo!</h3>`;

				setTimeout(() => {
					document.querySelector("#modalarca").style.display = "none";
				}, 1200);
			} else {
				estado.innerHTML = `<h3 style="color: red;">${data.mensaje}</h3>`;
			}
		});



	/* Funciones de los botones de los modal modificar Cantidad y Precio */

	BCerrarCant.onclick = () => {
		ModalCantidad.style.display = "none";
	};

	BCerrarPrec.onclick = () => {
		ModalPrecio.style.display = "none";
	};



	/* Funciones del boton Clientes */

	SearchBar_Client.onkeyup = async function () {
		var query = SearchBar_Client.value;  // Obtener valor ingresado
		var tabla = document.getElementById("TablaModalClient").getElementsByTagName('tbody')[0];

		// Realizar petición AJAX
		try {
			const url = urlTemplate.url_bClientes.replace('Cliente', query)
			const response = await fetch(url, {
				headers: {
					'X-Internal-Token': 'token-seguro-123',
					'Content-Type': 'application/json'
				},
			});
			const data = await response.json();

			vaciarTabla(tabla)

			// Insertar los nuevos resultados en la tabla
			data.clientes.forEach(cliente => {
				var nuevaFila = tabla.insertRow();
				var celdaCUIT = nuevaFila.insertCell(0);
				var celdaRazons = nuevaFila.insertCell(1);
				var celdaAccion = nuevaFila.insertCell(2);

				var boton = document.createElement("span");
				boton.textContent = "✅";
				boton.className = "emoji-clickable";
				boton.addEventListener("click", function () {
					seleccionarFilaCliente(this);
				});

				celdaCUIT.textContent = cliente.cuit;
				celdaRazons.textContent = cliente.razons;
				celdaAccion.appendChild(boton);
			});
		} catch (error) {
			mostrarAlerta('⚠️ Error de conexión. Intenta nuevamente.')
		}
	};

	BCliente.onclick = function () {
		ModalCliente.style.display = "block";
		SearchBar_Client.value = ''
		const cuerpo = TablaModalClient.querySelector("tbody");
		cuerpo.innerHTML = "";
	};

	cerrarModalClientes.onclick = function () {
		ModalCliente.style.display = "none";
	};

	function seleccionarFilaCliente(boton) {
		// Obtener la fila que contiene el botón
		const cuit = boton.parentNode.parentNode.cells[0].innerText;
		var letra
		// Llamada AJAX a Django para procesar los datos
		const url = urlTemplate.url_sCliente.replace('Cliente', cuit)
		fetch(url, {
			headers: {
				'X-Internal-Token': 'token-seguro-123',
				'Content-Type': 'application/json'
			},
		})
			.then(response => response.json())
			.then(data => {
				document.getElementById("razons").value = `${data.dato_cli[0].razons}`;
				document.getElementById("cuit").value = `${data.dato_cli[0].cuit}`;
				document.getElementById("dir").value = `${data.dato_cli[0].direccion}`;
				document.getElementById("resp").value = `${data.dato_cli[0].responsabilidad__descripcion}`;
				document.getElementById("list").value = `${data.dato_cli[0].lista__nombre}`;
				document.getElementById("BCliente").disabled = true;
				document.getElementById("BProductos").disabled = false;
				if (radio[0].checked === true) {
					if (data.dato_cli[0].responsabilidad__descripcion === 'RESPONSABLE INSCRIPTO') {
						letra = 1
					} else {

						letra = 6
					}
				} else {
					if (data.dato_cli[0].responsabilidad__descripcion === 'RESPONSABLE INSCRIPTO') {
						letra = 3
					} else {
						letra = 8
					}
				}
				fetch(`/api/internal/facturador/obt-nrofact?q=${letra}`, {
					headers: {
						'X-Internal-Token': 'token-seguro-123',
						'Content-Type': 'application/json'
					},
				})
					.then(res => res.json())
					.then(data => {
						document.getElementById("Nrofact").value = `${data.Nrofact}`;
						document.getElementById("ModalCliente").style.display = "none";
						Facturacheck.classList.add("readonly-switcher");
						Facturacheck1.classList.add("readonly-switcher");

					})
					.catch(error => console.error("Error en la solicitud:", error));


			})
			.catch(error => console.error("Error en la solicitud:", error));



	}


	/* Funciones del boton Productos */

	SearchBar_Products.onkeyup = async function () {
		var query = SearchBar_Products.value;  // Obtener valor ingresado
		var query2 = document.getElementById("list").value;
		var tabla = document.getElementById("TablaModalProductos").getElementsByTagName('tbody')[0];

		// Realizar petición AJAX
		try {
			const url = urlTemplate.url_bProductos.replace('Nombre', query).replace('Lista', query2)
			const response = await fetch(url, {
				headers: {
					'X-Internal-Token': 'token-seguro-123',
					'Content-Type': 'application/json'
				},
			})
			const data = await response.json();

			vaciarTabla(tabla)
			// Insertar los nuevos resultados en la tabla
			data.productos.forEach(producto => {
				var nuevaFila = tabla.insertRow();
				const input = document.createElement("input");
				var celdaNombre = nuevaFila.insertCell(0);
				var celdaCant = nuevaFila.insertCell(1);
				var celdaPrecio = nuevaFila.insertCell(2);
				var celdaIva = nuevaFila.insertCell(3);
				var celdaAccion = nuevaFila.insertCell(4);

				var boton = document.createElement("span");
				boton.textContent = "✅";
				boton.className = "emoji-clickable";
				boton.addEventListener("click", function () {
					const cuerpo = TablaProductos.querySelector("tbody");
					if (!input.classList.contains("invalido")) {
						if (!cuerpo || cuerpo.rows.length == 0) {
							agregarHeader(TablaProductos)
						}
						seleccionarFilaProducto(this, TablaProductos);
					}
				});

				celdaNombre.innerHTML = `<td>${producto.nombre}</td>`;

				input.type = "text";
				input.value = '1'
				input.contentEditable = true
				input.className = "input-celda";

				input.addEventListener("input", function () {
					const valor = input.value;
					if (!regex.test(valor)) {
						input.classList.add("invalido");
						boton.textContent = "❌";
						boton.disabled = true;
						boton.classList.add("sin-pointer");
					} else {
						input.classList.remove("invalido");
						boton.textContent = "✅";
						boton.disabled = false;
						boton.classList.remove("sin-pointer");
					}
				});
				celdaCant.appendChild(input)
				celdaPrecio.innerHTML = `<td>${producto.precio}</td>`;
				celdaIva.innerHTML = `<td>${producto.iva}</td>`;
				celdaAccion.appendChild(boton);
			})
		} catch {
			mostrarAlerta('⚠️ Error de conexión. Intenta nuevamente.')
		}
	};

	BProductos.onclick = function () {
		ModalProductos.style.display = "block";
		SearchBar_Products.value = ''
		const cuerpo = TablaModalProductos.querySelector("tbody");
		cuerpo.innerHTML = "";
	};

	document.getElementById("BCerrarProd").onclick = () => {
		ModalProductos.style.display = "none";
	};

	function seleccionarFilaProducto(boton, tabla) {
		// Obtener la fila que contiene el botón
		const fila = boton.closest("tr");
		const nombre = fila.cells[0].innerText;
		const cantidad = fila.cells[1].firstChild.value
		let precio = 0
		const iva = fila.cells[3].innerText;
		if (iva == '21.0') {
			precio = fila.cells[2].innerText / 1.21
		} else {
			precio = fila.cells[2].innerText / 1.105
		}
		const nuevaFila = tabla.insertRow();
		let aux = parseFloat(cantidad) * parseFloat(precio)


		// Celda: Descripción
		const CeldaDesc = nuevaFila.insertCell()
		const DescSpan = crearSpan()

		DescSpan.textContent = nombre
		CeldaDesc.appendChild(DescSpan);

		// Celda: Cantidad
		const celdaCantidad = nuevaFila.insertCell();
		const CantCont = crearContenedor()
		const CantSpan = crearSpan()
		const BotonCant = crearBoton()

		CantSpan.textContent = cantidad;
		BotonCant.textContent = "✏️";
		BotonCant.addEventListener("click", function () {
			ModalCantidad.style.display = "block";
			InputCant.value = cantidad
			InputCant.addEventListener("input", function () {
				const valor = InputCant.value;
				if (!regex.test(valor)) {
					InputCant.classList.add("invalido");
					BCerrarCant.disabled = true;
					BCerrarCant.classList.add("sin-pointer");
				} else {
					InputCant.classList.remove("invalido");
					BCerrarCant.disabled = false;
					BCerrarCant.classList.remove("sin-pointer");
				}
			});
		});

		CantCont.appendChild(CantSpan)
		CantCont.appendChild(BotonCant)
		celdaCantidad.appendChild(CantCont)

		// Celda: Precio unitario
		const celdaPreUn = nuevaFila.insertCell();
		const PreUnCont = crearContenedor()
		const PreUnSpan = crearSpan()
		const BotonPreUn = crearBoton()

		const PrecioR = redondearDecimales(precio, 4)
		PreUnSpan.textContent = PrecioR;
		BotonPreUn.textContent = "✏️";
		BotonPreUn.addEventListener("click", function () {
			ModalPrecio.style.display = "block";
			InputPrecio.value = PrecioR
			InputPrecio.addEventListener("input", function () {
				const valor = InputPrecio.value;
				if (!regex.test(valor)) {
					InputPrecio.classList.add("invalido");
					BCerrarPrec.disabled = true;
					BCerrarPrec.classList.add("sin-pointer");
				} else {
					InputPrecio.classList.remove("invalido");
					BCerrarPrec.disabled = false;
					BCerrarPrec.classList.remove("sin-pointer");
				}
			})
		});
		PreUnCont.appendChild(PreUnSpan)
		PreUnCont.appendChild(BotonPreUn)
		celdaPreUn.appendChild(PreUnCont)

		// Celda: Iva %
		const celdaIva = nuevaFila.insertCell();
		const IvaSpan = crearSpan()

		IvaSpan.textContent = iva
		celdaIva.appendChild(IvaSpan);


		// Celda: Total
		const celdaTotal = nuevaFila.insertCell();
		const TotalCont = crearContenedor()
		const TotalSpan = crearSpan()
		const TotalBoton = crearBoton()

		TotalSpan.textContent = redondearDecimales(aux, 2);
		TotalBoton.textContent = "❌";
		TotalBoton.addEventListener("click", function () {
			borrarContenido(this);
			CalcularFactura()
		});
		TotalCont.appendChild(TotalSpan);
		TotalCont.appendChild(TotalBoton);
		celdaTotal.appendChild(TotalCont);

		borrarContenido(boton)

		CalcularFactura()
		if (document.getElementById("Nrofact").value != '') {
			document.getElementById("btconfirmar").removeAttribute("disabled");
			generarJson()
		}
	}


	/* Funciones Auxiliares */

	function vaciarTabla(tabla) {
		while (tabla.firstChild) {
			tabla.removeChild(tabla.firstChild);
		}
	}

	function borrarContenido(boton) {
		const fila = boton.closest("tr");
		const cuerpo = TablaProductos.querySelector("tbody");
		fila.remove();
		SearchBar_Products.value = ''
		if (cuerpo.rows.length == 1) {
			TablaProductos.querySelector("tr").remove()
			document.getElementById("btconfirmar").setAttribute("disabled", true);
		}
	}

	function agregarHeader(tabla) {
		const filaEncabezado = tabla.insertRow();
		const encabezados = [
			"Descripción",
			"Cantidad",
			"Precio Unitario (s/iva)",
			"Iva %",
			"Total (s/iva)"
		];
		encabezados.forEach(texto => {
			const th = document.createElement("th");
			const span = document.createElement("span");
			span.textContent = texto;
			th.appendChild(span);
			filaEncabezado.appendChild(th);
		});
	}

	function redondearDecimales(valor, decimales) {
		const factor = Math.pow(10, decimales);
		const redondeado = Math.round(parseFloat(valor) * factor) / factor;
		return redondeado.toFixed(decimales);
	}



	function CalcularFactura() {
		var total21 = 0, total105 = 0, subtotal = 0
		var neto21 = 0, neto105 = 0

		for (let i = 1; i < TablaProductos.rows.length; i++) {
			let fila = TablaProductos.rows[i]
			let celda = fila.cells[4].querySelector("span").innerText
			let iva = fila.cells[3].querySelector("span").innerText
			subtotal += parseFloat(celda)
			if (iva == '21.0') {
				neto21 += parseFloat(celda)
				total21 += parseFloat(celda) * 0.21
			} else {
				neto105 += parseFloat(celda)
				total105 += parseFloat(celda) * 0.105
			}
		}

		document.getElementById('subtotal').innerHTML = `$ ${redondearDecimales(subtotal, 2)}`

		var total = subtotal + total21 + total105
		document.getElementById('iva21').value = `$ ${redondearDecimales(total21, 2)}`
		document.getElementById('iva105').value = `$ ${redondearDecimales(total105, 2)}`
		document.getElementById('neto21').value = `$ ${redondearDecimales(neto21, 2)}`
		document.getElementById('neto105').value = `$ ${redondearDecimales(neto105, 2)}`
		document.getElementById('total').value = `$ ${redondearDecimales(total, 2)}`
	}



	// Encapsulamiento de logica

	function crearContenedor() {
		const contenedor = document.createElement("div");
		contenedor.className = "celda-cantidad";
		return contenedor;
	}

	function crearSpan() {
		const span = document.createElement("span");
		span.className = "cantidad-texto";
		return span
	}

	function crearBoton() {
		const boton = document.createElement("button");
		boton.className = "btn-cantidad";
		return boton
	}

	function generarJson() {
		let datos = []
		for (let i = 1; i < TablaProductos.rows.length; i++) {
			let fila = TablaProductos.rows[i]
			let iva = parseFloat(fila.cells[3].querySelector("span").innerText)
			let subtotal = fila.cells[4].querySelector("span").innerText
			let totaliva = redondearDecimales((1 + (parseFloat(iva) / 100)) * parseFloat(subtotal), 2)
			let filaObj = {
				descripcion: fila.cells[0].querySelector("span").innerText,
				cantidad: fila.cells[1].querySelector("span").innerText,
				precio: fila.cells[2].querySelector("span").innerText,
				iva: iva,
				subtotal: subtotal,
				totaliva: totaliva
			};
			datos.push(filaObj);
		}
		inputJson = document.getElementById('inputJson')
		inputJson.value = JSON.stringify(datos)
	}

});
















