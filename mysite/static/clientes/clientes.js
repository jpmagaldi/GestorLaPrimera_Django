const cuitInput = document.getElementById("cuit");
const razonsInput = document.getElementById("razons");
const dirInput = document.getElementById("dir");
const provInput = document.getElementById("prov");
const aliasInput = document.getElementById("alias");
const listaInput = document.getElementById("lista");
const respInput = document.getElementById("resp");
const descuentoInput = document.getElementById("desc");
const recargoInput = document.getElementById("rec");
const oldCuit = document.getElementById("oldCuit");
const bCuit = document.getElementById("bCuit");

const searchBtton = document.getElementById("searchBtton");
const submitBtton = document.getElementById("submitBtton");

const accionInput = document.getElementById("accionInput");


cuitInput.addEventListener("input", () => {
	const valor = cuitInput.value.trim();

	const esValidoNum = /^[0-9]+$/.test(valor)

	if (!esValidoNum || valor.length > 11) {
		cuitInput.classList.add("input-error")
		searchBtton.disabled = true
		searchBtton.classList.add("cursor-error")
		submitBtton.disabled = true
		submitBtton.classList.add("button-error")
		cuitInput.setCustomValidity("Debe contener solo números (máximo 11 dígitos)")
		cuitInput.reportValidity();
	} else {
		cuitInput.classList.remove("input-error")
		submitBtton.classList.remove("button-error")
		searchBtton.classList.remove("cursor-error");
		searchBtton.disabled = false
		submitBtton.disabled = false
		cuitInput.setCustomValidity("")
	}
});

searchBtton.addEventListener("click", async () => {
	searchBtton.disabled = true
	cuitInput.readOnly = true

	const response = await fetch(`/api/internal/conectar-wsaa?q=ws_sr_constancia_inscripcion`, {
		headers: {
			'X-Internal-Token': 'token-seguro-123',
			'Content-Type': 'application/json'
		},
	})
	const response2 = await fetch(`/api/internal/abmclientes/buscar_clientes/?q=${cuitInput.value}`, {
		headers: {
			'X-Internal-Token': 'token-seguro-123',
			'Content-Type': 'application/json'
		},
	})
	const data = await response2.json()
	if (data.err2){
		window.location.href = `/api/internal/abmclientes/error_arca/?codigo=${data.codigo}`
      	return
	}
	if (data.err) {
		window.location.href = `/api/internal/abmclientes/error_arca/?codigo=${data.codigo}`
      	return
	}
	razonsInput.value = data.razons
	dirInput.value = data.dir
	provInput.value = data.prov
	respInput.value = data.resp
})

document.querySelectorAll(".button-table").forEach(boton => {
	boton.addEventListener("click", async () => {
		searchBtton.disabled = true
		searchBtton.classList.add("cursor-error")
		const fila = boton.closest("tr");
		const cuit = fila.querySelector(".campo-cuit").textContent.trim()
		oldCuit.value = cuit
		const response = await fetch(`/api/internal/abmclientes/editar_clientes?q=${cuit}`, {
			headers: {
				'X-Internal-Token': 'token-seguro-123',
				'Content-Type': 'application/json'
			},
		})
		const data = await response.json()
		cuitInput.value = cuit
		razonsInput.value = data.razons
		dirInput.value = data.dir
		provInput.value = data.prov
		aliasInput.value = data.alias
		listaInput.value = data.lista
		respInput.value = data.resp
		descuentoInput.value = parseFloat(data.desc).toFixed(2)
		recargoInput.value = parseFloat(data.rec).toFixed(2)
		submitBtton.textContent = 'Modificar'
		accionInput.value = 'Modificar'
		
	})
});


function confirmarAccion() {
  return confirm("¿Estás seguro que desea eliminar este cliente?");
}
