function yesnoCheck(that, target, targetInput) {
    if (that.value == "a") {
        document.getElementById(target).style.display = "block";
    } else {
        document.getElementById(targetInput).value = "";
        document.getElementById(target).style.display = "none";
    }
}

function brd(that, target, targetInput) {
    if (that.value == "b") {
        document.getElementById(targetInput).value = "";
        document.getElementById(target).style.display = "none";
    } else {
        document.getElementById(target).style.display = "block";
    }
}





function SaveCategory(cat, value){
	localStorage.setItem(cat, value);
}

function GetCategory(cat){
	return localStorage[cat];
}

function guardarCentroSecundario(url, slug) {
    if (GetCategory("quantity") == null) {
        SaveCategory("quantity", 1);
    }
    else {
        SaveCategory("quantity", Number(GetCategory("quantity")) + 1);
    }
    var quantity = Number(GetCategory("quantity"));
    var marca_catalogo = document.getElementById("marcaNumeroIdsec").value;
    var espacios_ocupados = document.getElementById("espaciosOcupadosIdSec").value;
    var estado_tablero_select = document.getElementById("estadoTableroIdSec");
    var estado_tablero = estado_tablero_select.options[estado_tablero_select.selectedIndex].value;
    var estado_tablero_especifique = document.getElementById("estadoTableroEspecifiqueIdSec").value;
    var ubicacion_select = document.getElementById("ubicacionIdSec");
    var ubicacion = ubicacion_select.options[ubicacion_select.selectedIndex].value;
    var canalizacion_select = document.getElementById("canalizacionIdSec");
    var canalizacion = canalizacion_select.options[canalizacion_select.selectedIndex].value;
    var canalizacion_especifique = document.getElementById("canalizacionEspecifiqueIdSec").value;
    var canalizacion_distancia = document.getElementById("canalizacionDistanciaIdSec").value;
    var estado_alimentadores_select = document.getElementById("estadoAlimentadoresIdSec");
    var estado_alimentadores = estado_alimentadores_select.options[estado_alimentadores_select.selectedIndex].value;
    var estado_alimentadores_especifique = document.getElementById("estadoAlimentadoresEspecifiqueIdSec").value;
    var estado_puesta_select = document.getElementById("estadoPuestaIdSec");
    var estado_puesta = estado_puesta_select.options[estado_puesta_select.selectedIndex].value;
    var estado_puesta_especifique = document.getElementById("estadoPuestaEspecifiqueIdSec").value;
    document.getElementById("marcaNumeroIdsec").value = "";
    document.getElementById("espaciosOcupadosIdSec").value = "";
    document.getElementById("estadoTableroIdSec").value = "b";
    document.getElementById("estadoTableroEspecifiqueIdSec").value = "";
    document.getElementById("canalizacionIdSec").value = "b";
    document.getElementById("canalizacionEspecifiqueIdSec").value = "";
    document.getElementById("canalizacionDistanciaIdSec").value = "";
    document.getElementById("estadoAlimentadoresIdSec").value = "b";
    document.getElementById("estadoAlimentadoresEspecifiqueIdSec").value = "";
    document.getElementById("estadoPuestaIdSec").value = "b";
    document.getElementById("estadoPuestaEspecifiqueIdSec").value = "";


    $.ajax({
        type: 'POST',
        url: url,
        data: { "marca_catalogo": marca_catalogo,
            "espacios_ocupados": espacios_ocupados,
            "estado_tablero": estado_tablero,
            "estado_tablero_especifique": estado_tablero_especifique,
            "ubicacion": ubicacion,
            "canalizacion": canalizacion,
            "canalizacion_especifique": canalizacion_especifique,
            "canalizacion_distancia": canalizacion_distancia,
            "estado_alimentadores": estado_alimentadores,
            "estado_alimentadores_especifique": estado_alimentadores_especifique,
            "estado_puesta": estado_puesta,
            "estado_puesta_especifique": estado_puesta_especifique,
            "quantity": quantity,
            csrfmiddlewaretoken: jQuery("[name=csrfmiddlewaretoken]").val()
        },
        success: function (response) {
            // if not valid user, alert the user
            if (response["scc"]){
                htmlTextModify()
            }
        },
        error: function (response) {
            console.log(response);
        }
    });
}

function setInitialCategory() {
    SaveCategory("quantity", 0);
}

function htmlTextModify(){
	var quantity = Number(GetCategory("quantity"));
	if (quantity > 1) {
	     document.getElementById('messages').innerHTML = '<p>' + quantity + ' centros de carga secundarios añadidos</p>';
    }
	else {
	    if (quantity == 1) {
	        document.getElementById('messages').innerHTML = 'Un centro secundario de carga añadido</p>';
        }
    }
}

