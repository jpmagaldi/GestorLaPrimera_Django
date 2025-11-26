document.addEventListener("DOMContentLoaded", () => {

	const urlTemplate = JSON.parse(
		document.getElementById("url-template").textContent
	);


	const btnBuscar = document.getElementById('btnBuscar')
	const labelInfo = document.getElementById('labelInfo')
	const tabla = document.getElementById("tablaReportes")
	const Fechafininput = document.getElementById("fechaFin");
	const FechaFin = flatpickr("#fechaFin", {
		dateFormat: "d-m-Y",
		locale: 'es',
		onClose: function (selectedDates, dateStr, instance) {
			btnBuscar.disabled = false
		}
	});
	const FechaInicio = flatpickr("#fechaInicio", {
		dateFormat: "d-m-Y",
		locale: 'es',
		onClose: function (selectedDates, dateStr, instance) {
			FechaFin.set("minDate", selectedDates[0]);
			Fechafininput.disabled = false
			Fechafininput.classList.remove('cursor-notallowed')

		}
	});
	Fechafininput.disabled = true
	Fechafininput.classList.add('cursor-notallowed')
	btnBuscar.disabled = true
			
	btnBuscar.onclick = async function () {
		const response = await fetch(
			urlTemplate.url_reportFecha
				.replace("fechaIni", FechaInicio.input.value)
				.replace("fechaFin", FechaFin.input.value), {
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



})