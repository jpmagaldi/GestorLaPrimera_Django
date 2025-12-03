document.addEventListener("DOMContentLoaded", () => {

	const urlTemplate = JSON.parse(
		document.getElementById("url-template").textContent
	);

	const inputRazon = document.getElementById('inputRazon')
	const btnBuscar = document.getElementById('btnBuscar')
	const labelInfo = document.getElementById('labelInfo')
	const tabla = document.getElementById("tablaReportes")
	const Fechafininput = document.getElementById("fechaFin");
	const FechaFin = flatpickr("#fechaFin", {
		dateFormat: "d-m-Y",
		locale: 'es',
		onClose: function (selectedDates, dateStr, instance) {
			btnBuscar.disabled = false
		},
	});
	const FechaInicio = flatpickr("#fechaInicio", {
		dateFormat: "d-m-Y",
		locale: 'es',
		onClose: function (selectedDates, dateStr, instance) {
			FechaFin.set("minDate", selectedDates[0]);
			Fechafininput.disabled = false
			Fechafininput.classList.remove('cursor-notallowed')
		},
	});

	const checks = document.querySelectorAll(".chk-unico");

	Fechafininput.disabled = true
	Fechafininput.classList.add('cursor-notallowed')


	var Url = null

	const grupoFecha = document.getElementById('grupoFechas')
	const grupoCliente = document.getElementById('grupoCliente')
	var opcion = 'grupoFechas'
	grupoFecha.classList.add('activo');

	checks.forEach(chk => {
		chk.addEventListener("change", () => {
			grupoCliente.classList.remove('activo');
			grupoFecha.classList.remove('activo');

			document.querySelectorAll('.chk-unico').forEach(c => {
				if (c !== chk) {
					c.checked = false
				}
			});
			if (chk.checked) {
				btnBuscar.disabled = false
				switch (chk.name) {
					case 'grupoFechas': {
						grupoFecha.classList.add('activo');
						opcion = 'grupoFecha'
						break
					}
					case 'grupoCliente': {
						grupoCliente.classList.add('activo');
						opcion = 'grupoCliente'
						break
					}
					case 'ChkAmbos': {
						grupoCliente.classList.add('activo');
						grupoFecha.classList.add('activo');
						opcion = 'grupoAmbos'
						break
					}
				}
			} else {
				btnBuscar.disabled = true
			}
		});
	});


	btnBuscar.onclick = async function () {
		document.getElementById('boxunico').classList.add('noactivo')
		grupoCliente.classList.remove('activo');
		grupoFecha.classList.remove('activo');

		switch (opcion) {
			case 'grupoFechas': {
				Url = urlTemplate.url_reportFechaFSR
					.replace("fechaIni", FechaInicio.input.value)
					.replace("fechaFin", FechaFin.input.value)
				break
			}
			case 'grupoCliente': {
				Url = urlTemplate.url_reportFechaRSF
					.replace("razonS", inputRazon.value)
				break
			}
			case 'grupoAmbos': {
				Url = urlTemplate.url_reportFechaFCR
					.replace("fechaIni", FechaInicio.input.value)
					.replace("fechaFin", FechaFin.input.value)
					.replace("razonS", inputRazon.value)
				break
			}
		}
		try {
			const response = await fetch(
				Url, {
				headers: {
					'X-Internal-Token': 'token-seguro-123',
					'Content-Type': 'application/json'
				},
			})
			const data = await response.json();

			btnBuscar.disabled = true
			if (!data.facturas) {
				labelInfo.classList.add("visible")
			}
			else {
				for (let i = 0; i < data.facturas.length; i++) {
					const fila = tabla.insertRow();
					const element = data.facturas[i]

					const celdaFecha = fila.insertCell();
					celdaFecha.textContent = element.fecha.split("-").reverse().join("-");
					const celdaComp = fila.insertCell();
					celdaComp.textContent = element.comprobante__descripcion;
					const celdaN_fact = fila.insertCell();
					celdaN_fact.textContent = element.n_fact;
					const celdaCliente = fila.insertCell();
					celdaCliente.textContent = element.cliente__razons;
					const celdaTotal = fila.insertCell();
					celdaTotal.textContent = element.total;

					const celdaAcc = fila.insertCell();
					celdaAcc.classList.add("acciones");
					const spnVer = document.createElement("button");
					spnVer.classList.add('material-icons')
					spnVer.classList.add('spanButton')
					spnVer.textContent = 'visibility'

					spnVer.addEventListener("click", () => {
						const url = urlTemplate.url_verFactura
							.replace("Comprobante", element.comprobante__descripcion)
							.replace("Nro", element.n_fact);
						window.location.href = url;
					})


					celdaAcc.appendChild(spnVer);
				}
			}
		}
		catch { labelInfo.classList.add("visible") }
	}


})